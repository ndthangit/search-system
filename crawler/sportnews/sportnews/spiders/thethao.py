import scrapy
import re

class SportSpider(scrapy.Spider):
    name = "thethao"
    allowed_domains = ["vnexpress.net"]
    start_urls = ["https://vnexpress.net/the-thao"]

    def parse(self, response):
        for article in response.css(".item-news"):
            link_elem = article.css("h2.title-news a, h3.title-news a")
            summary_elem = article.css("p.description a")

            title = link_elem.css("::text").get()
            link = link_elem.css("::attr(href)").get()
            data_medium = link_elem.css("::attr(data-medium)").get()

            summary_nodes = summary_elem.xpath("text()").getall()
            summary = " ".join(t.strip() for t in summary_nodes if t.strip())

            if title and link:
                match = re.search(r"-([0-9]+)\.html", link)
                article_id = match.group(1) if match else None

                yield response.follow(link, callback=self.parse_detail, meta={
                    "title": title.strip(),
                    "link": link.strip(),
                    "data_medium": data_medium,
                    "summary": summary,
                    "article_id": article_id,
                })

        next_page = response.css("a.btn-page.next-page::attr(href)").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_detail(self, response):
        paragraphs = response.css("article.fck_detail p::text").getall()
        content = " ".join(p.strip() for p in paragraphs if p.strip())

        yield {
            "title": response.meta["title"],
            "link": response.meta["link"],
            "data_medium": response.meta["data_medium"],
            "summary": response.meta["summary"],
            "article_id": response.meta["article_id"],
            "content": content,
        }
