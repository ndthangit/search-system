import json
import os
import re
import scrapy
import hashlib

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from twisted.internet import defer
from scrapy import signals
from random import sample
from datetime import timedelta

from app.services.scrapy_es_adapter import ScrapyElasticAdapter

STATE_FILE = "data/state.json"
ES_INDEX = "articles-json"
RANDOM_CHECK_SIZE = 30
RANDOM_CHECK_DAYS = 1

def extract_article_id(link: str) -> str:
    match = re.search(r"(\d{17})\.htm", link)
    if match:
        return match.group(1)
    return link

def hash_content(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class SportNewsSpider(scrapy.Spider):
    name = "sport_news"
    allowed_domains = ["dantri.com.vn"]
    start_urls = ["https://dantri.com.vn/rss/the-thao.rss"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_service = ScrapyElasticAdapter()
        self.last_pub_ts = None
        self.max_pub_ts = None
        self.existing_docs = {}
        self.validation_complete = False

        # Load state
        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                ts = json.load(f).get("last_pub_ts")
                if ts:
                    self.last_pub_ts = datetime.fromisoformat(ts)

    @classmethod
    def from_crawler(cls, crawler, *args, **kwargs):
        spider = super().from_crawler(crawler, *args, **kwargs)
        crawler.signals.connect(spider.on_spider_opened, signal=signals.spider_opened)
        return spider

    def on_spider_opened(self):
        self.logger.info("Spider opened → start ES validation")
        defer.ensureDeferred(self._validate_existing_docs())

    async def _validate_existing_docs(self):
        try:
            result = await self.es_service.search_match(
                ES_INDEX,
                {
                    "query": {"match_all": {}},
                    "size": 1000000,
                    "_source": ["link", "content", "content_hash", "last_updated"]
                }
            )

            hits = result.get("hits", {}).get("hits", [])
            self.logger.info(f"Found {len(hits)} ES documents")

            for hit in hits:
                link = hit["_source"].get("link", hit["_id"])
                doc_id = extract_article_id(link)

                req = scrapy.Request(
                    url=link,
                    method="HEAD",
                    errback=self._head_err,
                    meta={"doc_id": doc_id},
                    dont_filter=True
                )

                self.crawler.engine.crawl(req)

            # After checking dead links, do random content update checks
            await self._random_check_update(result)

        except Exception as e:
            self.logger.error(f"ES validation failed: {e}")

        self.validation_complete = True
        self.logger.info("ES validation complete")

   # delete if link not reachable
    def _head_err(self, failure):
        doc_id = failure.request.meta["doc_id"]
        self.logger.info(f"Dead link detected, deleting ES doc: {doc_id}")
        d = defer.ensureDeferred(self.es_service.delete_doc(ES_INDEX, doc_id))
        return d

    # get some random links and get content to check update
    async def _random_check_update(self, result):
        self.logger.info("Start random_check_update")

        hits = result.get("hits", {}).get("hits", [])
        if not hits:
            self.logger.info("No docs eligible for random check")
            return

        now = datetime.now(timezone.utc)
        threshold = now - timedelta(days=RANDOM_CHECK_DAYS)

        stale_docs = []
        recent_docs = []

        for hit in hits:
            src = hit.get("_source", {})
            last_updated_raw = src.get("last_updated")

            if not last_updated_raw:
                stale_docs.append(hit)
                continue

            try:
                last_updated = datetime.fromisoformat(last_updated_raw)
            except Exception:
                stale_docs.append(hit)
                continue

            if last_updated < threshold:
                stale_docs.append(hit)
            else:
                recent_docs.append(hit)

        candidates = []

        # Phase 1:
        if stale_docs:
            candidates.extend(
                sample(
                    stale_docs,
                    min(RANDOM_CHECK_SIZE, len(stale_docs))
                )
            )

        # Phase 2:
        remaining = RANDOM_CHECK_SIZE - len(candidates)
        if remaining > 0 and recent_docs:
            candidates.extend(
                sample(
                    recent_docs,
                    min(remaining, len(recent_docs))
                )
            )

        self.logger.info(
            f"Random check {len(candidates)} documents "
            f"(stale={len(stale_docs)}, recent={len(recent_docs)})"
        )

        for hit in candidates:
            src = hit["_source"]
            doc_id = hit["_id"]

            req = scrapy.Request(
                url=src["link"],
                callback=self._parse_check_update,
                meta={
                    "doc_id": doc_id,
                    "old_hash": src.get("content_hash"),
                },
                dont_filter=True
            )

            self.crawler.engine.crawl(req)

    def _parse_check_update(self, response):
        doc_id = response.meta["doc_id"]
        old_hash = response.meta["old_hash"]

        paragraphs = response.css("article.singular-container p::text").getall()
        content_text = " ".join(p.strip() for p in paragraphs if p.strip())
        new_hash = hash_content(content_text)

        if new_hash == old_hash:
            self.logger.info(f"[NO CHANGE] {doc_id}")
            return

        self.logger.info(f"[UPDATED] {doc_id}")

        item = {
            "doc_id": doc_id,
            "content": content_text,
            "content_hash": new_hash,
            "last_updated": datetime.now(timezone.utc).isoformat()
        }

        defer.ensureDeferred(
            self.es_service.index_data(ES_INDEX, doc_id, item)
        )

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        if not self.validation_complete:
            yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
            return

        for item in response.xpath("//item"):
            pub_raw = item.xpath("pubDate/text()").get()
            if not pub_raw:
                continue

            pub_ts = parsedate_to_datetime(pub_raw).astimezone(timezone.utc)

            if self.last_pub_ts and pub_ts <= self.last_pub_ts:
                self.logger.debug(
                    f"Skip old article: {pub_ts.isoformat()} <= {self.last_pub_ts.isoformat()}"
                )
                continue

            link = item.xpath("link/text()").get()
            title = item.xpath("title/text()").get()
            description = item.xpath("description/text()").get()

            if not link or not title:
                continue

            if self.max_pub_ts is None or pub_ts > self.max_pub_ts:
                self.max_pub_ts = pub_ts

            yield scrapy.Request(
                link,
                callback=self.parse_detail,
                meta={
                    "link": link,
                    "title": title.strip(),
                    "summary": self._clean_html(description),
                    "pub_ts": pub_ts.isoformat(),
                },
                dont_filter=True
            )

    def parse_detail(self, response):
        doc_id = extract_article_id(response.meta["link"])

        paragraphs = response.css("article.singular-container p::text").getall()
        content_text = " ".join(p.strip() for p in paragraphs if p.strip())
        full_content = response.meta["summary"] + content_text

        item = {
            "doc_id": doc_id,
            "title": response.meta["title"],
            "link": response.meta["link"],
            "summary": response.meta["summary"],
            "content": full_content,
            "length": len(full_content),
            "content_hash": hash_content(full_content),
            "last_updated": response.meta["pub_ts"],
            "pub_ts": response.meta["pub_ts"],
        }

        defer.ensureDeferred(self._index_es(item))
        yield item

    def _index_es(self, item):
        doc_id = item["doc_id"]
        self.logger.info(f"New ES doc: {doc_id}")

        d = self.es_service.index_data(ES_INDEX, doc_id, item)
        return d

    def closed(self, reason):
        if self.max_pub_ts:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "last_pub_ts": self.max_pub_ts.isoformat(),
                    },
                    f,
                    indent=2,
                    ensure_ascii=False
                )

    @staticmethod
    def _clean_html(text):
        if not text:
            return ""
        return re.sub(r"<[^>]+>", "", text).strip()
