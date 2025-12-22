import scrapy

class HustFeedSpider(scrapy.Spider):
    name = "hust_feeds"
    allowed_domains = ["hust.edu.vn"]
    start_urls = ["https://hust.edu.vn/vi/feeds/"]

    def parse(self, response):
        page_links = response.css(
            ".tree.well a::attr(href)"
        ).getall()

        for link in page_links:
            if link.endswith("/rss/"):
                yield response.follow(link, callback=self.parse_rss)

    def parse_rss(self, response):
        items = response.xpath("//item")

        for item in items:
            title = item.xpath("title/text()").get()
            link = item.xpath("link/text()").get()
            description = item.xpath("description/text()").get()

            if link:
                yield response.follow(
                    link,
                    callback=self.parse_detail,
                    meta={
                        "title": title,
                        "link": link,
                        "description": description,
                        "rss_source": response.url,
                    }
                )

    def parse_detail(self, response):
        panel = response.css("div.panel-body")

        content_text = panel.xpath("string(.)").get()
        content_text = " ".join(content_text.split())

        yield {
            "title": response.meta["title"],
            "link": response.meta["link"],
            "description": response.meta["description"],
            "rss_source": response.meta["rss_source"],
            "content_html": content_text,
        }

