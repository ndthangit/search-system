import json
import os
import re
import scrapy
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

STATE_FILE = "data/state.json"


class SportNewsSpider(scrapy.Spider):
    name = "sport_news"
    allowed_domains = ["dantri.com.vn"]
    start_urls = ["https://dantri.com.vn/rss/the-thao.rss"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_pub_ts: datetime | None = None
        self.max_pub_ts: datetime | None = None
        self.stop_crawl = False

        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                ts = json.load(f).get("last_pub_ts")
                if ts:
                    self.last_pub_ts = datetime.fromisoformat(ts)

    def parse(self, response):
        items = response.xpath("//item")

        for item in items:
            pub_date_raw = item.xpath("pubDate/text()").get()
            if not pub_date_raw:
                continue

            pub_ts = parsedate_to_datetime(pub_date_raw).astimezone(timezone.utc)

            # Stop when reach old news
            if self.last_pub_ts and pub_ts <= self.last_pub_ts:
                self.stop_crawl = True
                break

            link = item.xpath("link/text()").get()
            title = item.xpath("title/text()").get()
            category = item.xpath("category/text()").get()
            description = item.xpath("description/text()").get()

            if not link or not title:
                continue

            if self.max_pub_ts is None or pub_ts > self.max_pub_ts:
                self.max_pub_ts = pub_ts

            yield scrapy.Request(
                url=link,
                callback=self.parse_detail,
                meta={
                    "title": title.strip(),
                    "link": link.strip(),
                    "summary": self._clean_html(description),
                    "category": category,
                    "pub_ts": pub_ts.isoformat(),
                },
            )

        if self.stop_crawl:
            self.logger.info("Reached last pubDate, stop RSS parsing.")

    def parse_detail(self, response):
        paragraphs = response.css("article.fck_detail p::text").getall()
        content = " ".join(p.strip() for p in paragraphs if p.strip())

        yield {
            "title": response.meta["title"],
            "link": response.meta["link"],
            "summary": response.meta["summary"],
            "content": content,
            "category": response.meta["category"],
            "pub_ts": response.meta["pub_ts"],
            "crawled_at": datetime.utcnow().isoformat(),
        }

    def closed(self, reason):
        if self.max_pub_ts:
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

            state = {
                "last_pub_ts": self.max_pub_ts.isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved last_pub_ts = {self.max_pub_ts.isoformat()}")

    @staticmethod
    def _clean_html(text: str | None) -> str:
        if not text:
            return ""
        return re.sub(r"<[^>]+>", "", text).strip()
