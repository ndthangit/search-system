import scrapy


class HustSpider(scrapy.Spider):
    name = "hust"
    allowed_domains = ["hust.edu.vn"]
    start_urls = ["https://www.hust.edu.vn/vi/feeds"]

    # Cấu hình để tránh bị block
    custom_settings = {
        'DOWNLOAD_DELAY': 5,  # Đợi 5 giây giữa mỗi request
        'RANDOMIZE_DOWNLOAD_DELAY': True,  # Random trong khoảng 2.5s đến 7.5s (tránh bị phát hiện là bot)
        'CONCURRENT_REQUESTS_PER_DOMAIN': 1,  # Chỉ gửi 1 yêu cầu tại một thời điểm cho domain này
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        # Lấy các link trong danh sách tin tức/RSS
        links = response.xpath('//li//a/@href').getall()
        for link in links:
            if link:
                link = link.strip()
                if link.startswith(('javascript:', 'mailto:', 'tel:', '#')):
                    continue

                # Truy cập từng link và chờ 5s (theo custom_settings)
                yield response.follow(link, callback=self.parse_detail)

    def parse_detail(self, response):
        # Trích xuất dữ liệu sạch
        nodes = response.xpath(
            '//div[contains(@class, "content")]//text() | //article//text() | //body//text()').getall()
        clean_text = [t.strip() for t in nodes if t.strip()]
        body_text = ' '.join(clean_text)

        yield {
            'url': response.url,
            'title': response.xpath('//title/text()').get(default='').strip(),
            'body': body_text[:1000]  # Lấy 1000 ký tự đầu để file output gọn gàng
        }