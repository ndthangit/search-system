import scrapy
import re
import json
import os
from datetime import datetime

STATE_FILE = "data/state.json"

class SportSpider(scrapy.Spider):
    name = "thethao"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/the-thao"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.last_link = None
        self.new_last_link = None
        self.stop_crawl = False

        if os.path.exists(STATE_FILE):
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                self.last_link = json.load(f).get("last_link")

    def parse(self, response):
        for article in response.css(".item-news"):
            link_elem = article.css("h2.title-news a, h3.title-news a")
            summary_elem = article.css("p.description a")

            title = link_elem.css("::text").get()
            link = link_elem.css("::attr(href)").get()
            data_medium = link_elem.css("::attr(data-medium)").get()

            if not title or not link:
                continue

            if self.last_link and link == self.last_link:
                self.stop_crawl = True
                return

            if self.new_last_link is None:
                self.new_last_link = link

            summary = " ".join(
                t.strip() for t in summary_elem.xpath("text()").getall() if t.strip()
            )

            match = re.search(r"-([0-9]+)\.html", link)
            article_id = match.group(1) if match else None

            yield response.follow(
                link,
                callback=self.parse_detail,
                meta={
                    "title": title.strip(),
                    "link": link.strip(),
                    "data_medium": data_medium,
                    "summary": summary,
                    "article_id": article_id,
                },
            )

        if not self.stop_crawl:
            next_page = response.css("a.btn-page.next-page::attr(href)").get()
            if next_page:
                yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        paragraphs = response.css("article.fck_detail p::text").getall()
        content = " ".join(p.strip() for p in paragraphs if p.strip())

        self.logger.info(f'Already crawl {response.meta["link"]}')
        yield {
            "title": response.meta["title"],
            "link": response.meta["link"],
            "summary": response.meta["summary"],
            "article_id": response.meta["article_id"],
            "content": content,
        }

    def closed(self, reason):
        if self.new_last_link:
            state = {
                "last_link": self.new_last_link,
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            }
            os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
            with open(STATE_FILE, "w", encoding="utf-8") as f:
                json.dump(state, f, ensure_ascii=False, indent=2)

            self.logger.info(f"Saved new state: {self.new_last_link}")

