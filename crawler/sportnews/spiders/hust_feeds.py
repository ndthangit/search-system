import scrapy
import json
import os
from datetime import datetime

STATE_FILE = "data/hust_state.json"

class HustFeedSpider(scrapy.Spider):
    name = "hust_feeds"
    allowed_domains = ["hust.edu.vn"]
    start_urls = ["https://hust.edu.vn/vi/feeds/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.state = {}
        self.new_state = {}

        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                self.state = json.load(f)

    def parse(self, response):
        rss_links = response.css(".tree.well a::attr(href)").getall()

        for rss_url in rss_links:
            if rss_url.endswith("/rss/"):
                yield response.follow(
                    rss_url,
                    callback=self.parse_rss,
                    meta={"rss_url": rss_url},
                )

    def parse_rss(self, response):
        rss_url = response.meta["rss_url"]
        last_link = self.state.get(rss_url, {}).get("last_link")

        items = response.xpath("//item")

        for item in items:
            title = item.xpath("title/text()").get()
            link = item.xpath("link/text()").get()

            if not link:
                continue

            if last_link and link == last_link:
                self.logger.info(f"Stop RSS {rss_url}")
                break

            if rss_url not in self.new_state:
                self.new_state[rss_url] = {
                    "last_link": link,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                }

            yield response.follow(
                link,
                callback=self.parse_detail,
                meta={
                    "title": title,
                    "link": link,
                    "rss_source": rss_url,
                }
            )

    def parse_detail(self, response):
        panel = response.css("div.panel-body")
        content_text = panel.xpath("string(.)").get() or ""
        content_text = " ".join(content_text.split())

        yield {
            "title": response.meta["title"],
            "link": response.meta["link"],
            "rss_source": response.meta["rss_source"],
            "content": content_text,
        }

    def closed(self, reason):
        if not self.new_state:
            return

        os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

        self.state.update(self.new_state)

        with open(STATE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.state, f, ensure_ascii=False, indent=2)

        self.logger.info(f"Saved state for {len(self.new_state)} RSS feeds")
