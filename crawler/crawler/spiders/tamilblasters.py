#'https://www.1tamilblasters.re/index.php?/forums/topic/77652-secondary-home-page-2023/'
import scrapy
from scrapy.linkextractors import LinkExtractor
import time
from datetime import datetime


class CrawlingSpider(scrapy.Spider):
    name = "spidie"
    allowed_domains = ["1tamilblasters.team"]
    start_urls = ["https://www.1tamilblasters.team/index.php?/forums/topic/77652-secondary-home-page-2023/", "https://www.1tamilblasters.team/index.php?/forums/topic/41822-secondary-home-page-2022/"]
    # rules = (
    #     Rule(LinkExtractor(allow=(r"index\.php\?/forums/topic",)), callback="parse"),
    # )

    def parse(self, response):
        links = LinkExtractor(allow=(r'index\.php\?/forums/topic',)).extract_links(response)
        for link in links:
            url = link.url
            print(url)
            yield response.follow(url, callback=self.parse_link)

    def parse_link(self, response):
        time.sleep(0.5)
        title = response.xpath('//*[@id="ipsLayout_mainArea"]/div[2]/div[3]/div/h1/span/span/text()').get()
        magnet_link = response.css('a.magnet-plugin::attr(href)').get()
        time_of_upload = response.css('.ipsType_normal time::attr(datetime)').get()
        
        self.log(f'Visited {response.url}')
        yield {
            'title': title,
            'time_of_upload': time_of_upload,
            'magnet_link': magnet_link,
        }

        