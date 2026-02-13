from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class MercatusCenter(OCSpider):
    name = 'MercatusCenter'
    
    country = "US"

    proxy_country = "us"

    HEADLESS_BROWSER_WAIT_TIME = 10000   # 10 seconds wait time

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.HeadlessBrowserProxy': 350
            },
        "DOWNLOAD_DELAY": 1
    }

    start_urls_names = {
        'https://www.mercatus.org/research': 'Articles'
    }
    
    charset = "utf-8"
    
    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Eastern"
    
    def get_articles(self, response) :
        return response.xpath('//h3[@class="coh-heading coh-style-heading-5-size"]/a/@href').getall()
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[contains(@class, "heading__text")]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date = response.xpath('normalize-space(//time[@class="coh-inline-element"]/text())').get()
        if date:
            try:
                dt = datetime.strptime(date, self.date_format())
                return dt.strftime(self.date_format()) 
            except ValueError:
                pass
        return ""

    def get_authors(self, response):
        return response.xpath('//div[@class="coh-style-byline"]//ul/li/a/text()').get()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None