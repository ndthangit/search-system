import json
import os
import re
import scrapy

from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from twisted.internet import defer
from scrapy import signals

from app.services.scrapy_es_adapter import ScrapyElasticAdapter

STATE_FILE = "data/state.json"
ES_INDEX = "articles-json"

def extract_article_id(link: str) -> str:
    match = re.search(r"(\d{17})\.htm", link)
    if match:
        return match.group(1)
    return link


class SportNewsSpider(scrapy.Spider):
    name = "sport_news"
    allowed_domains = ["dantri.com.vn"]
    start_urls = ["https://dantri.com.vn/rss/the-thao.rss"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.es_service = ScrapyElasticAdapter()
        self.last_pub_ts = None
        self.max_pub_ts = None
        self.existing_docs = {}  # doc_id -> {doc_id, content_length}
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
                    "size": 10000,
                    "_source": ["link", "content"]
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
                    callback=self._head_check,
                    errback=self._head_err,
                    meta={"doc_id": doc_id},
                    dont_filter=True
                )

                # Chỉ gọi crawl mà không cần spider=...
                self.crawler.engine.crawl(req)

        except Exception as e:
            self.logger.error(f"ES validation failed: {e}")

        self.validation_complete = True
        self.logger.info("ES validation complete")

    def _head_check(self, response):
        doc_id = response.meta.get("doc_id", extract_article_id(response.url))
        content_length_header = response.headers.get("Content-Length")
        try:
            content_length = int(content_length_header) if content_length_header else None
        except ValueError:
            content_length = None

        self.existing_docs[doc_id] = {
            "doc_id": doc_id,
            "content_length": content_length
        }
        self.logger.debug(f"Link alive: {response.url}, content-length={content_length}")

    def _head_err(self, failure):
        doc_id = failure.request.meta["doc_id"]
        self.logger.info(f"Dead link detected, deleting ES doc: {doc_id}")
        d = defer.ensureDeferred(self.es_service.delete_doc(ES_INDEX, doc_id))
        return d

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
        content_bytes = response.body
        length_bytes_raw = len(content_bytes)

        paragraphs = response.css("article.singular-container p::text").getall()
        content_text = " ".join(p.strip() for p in paragraphs if p.strip())

        item = {
            "doc_id": doc_id,
            "title": response.meta["title"],
            "link": response.meta["link"],
            "summary": response.meta["summary"],
            "content": content_text + response.meta["summary"],
            "last_updated": response.meta["pub_ts"],
            "pub_ts": response.meta["pub_ts"],
            "length": length_bytes_raw
        }

        defer.ensureDeferred(self._index_es(item))
        yield item

    def _index_es(self, item):
        doc_id = item["doc_id"]

        old = self.existing_docs.get(doc_id)

        # Nếu content_length giống, skip
        if old and old["content_length"] == item["length"]:
            self.logger.info(f"Skip unchanged: {doc_id}")
            return defer.succeed(None)

        if old:
            item["updated_at"] = datetime.utcnow().isoformat()
            self.logger.info(f"Update ES: {doc_id}")
        else:
            self.logger.info(f"New ES doc: {doc_id}")

        d = self.es_service.index_data(ES_INDEX, doc_id, item)

        def _done(_):
            self.existing_docs[doc_id] = {
                "doc_id": doc_id,
                "content_length": item["length"]
            }

        d.addCallback(_done)
        return d

    def closed(self, reason):
        if self.max_pub_ts:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(
                    {
                        "last_pub_ts": self.max_pub_ts.isoformat(),
                        "updated_at": datetime.utcnow().isoformat(),
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
