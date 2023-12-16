#'https://www.1tamilblasters.re/index.php?/forums/topic/77652-secondary-home-page-2023/'
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
import time
from datetime import datetime


class CrawlingSpider(CrawlSpider):
    name = "spidie"
    allowed_domains = ["1tamilblasters.re"]
    start_urls = ["https://www.1tamilblasters.re/index.php?/forums/topic/77652-secondary-home-page-2023/"]
    rules = (
        Rule(LinkExtractor(allow=(r"index\.php\?/forums/topic",)), callback="parse"),
    )


    def parse(self, response):
        time.sleep(3)
        title = response.xpath('//*[@id="ipsLayout_mainArea"]/div[2]/div[3]/div/h1/span/span/text()').get()
        magnet_link = response.css('a.magnet-plugin::attr(href)').get()
        time_of_upload = response.css('.ipsType_normal time::attr(datetime)').get()
        date_object = datetime.fromisoformat(time_of_upload.replace("Z", "+00:00"))
        
        self.log(f'Visited {response.url}')
        yield {
            'title': title,
            'time_of_upload': time_of_upload,
            'magnet_link': magnet_link,
        }

        