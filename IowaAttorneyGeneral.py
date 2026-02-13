from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class IowaAttorneyGeneral(OCSpider):
    name = "IowaAttorneyGeneral"

    country = "US"
    
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350
        },
        "DOWNLOAD_DELAY": 5,
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter',
    }
    
    HEADLESS_BROWSER_WAIT_TIME = 30000  # 30 Seconds wait time

    start_urls_names = {
        "https://www.iowaattorneygeneral.gov/newsroom": "Newsroom",
    }
    
    charset = "utf-8"

    @property
    def language(self): 
        return "English"

    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def timezone(self):
        return "America/Chicago"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="cms_metadata1 cms_title"]/h3/a/@href').getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="cms_metadata1 cms_title"]/h1/text()').get().strip()

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="cms_content"]//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        date_str = (response.xpath('//div[@class="cms_metadata2 cms_date"]/h3/text()').get()).strip()
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%m-%d-%Y") 
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//td[@class="right"]//a[contains(@id, "next")]/@href').get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None