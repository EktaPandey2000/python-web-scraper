from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class TexasComptrollerOfPublicAccounts(OCSpider):
    name = "TexasComptrollerOfPublicAccount"

    country="US"

    start_urls_names = {
        "https://comptroller.texas.gov/about/media-center/news/": "News Releases",
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
        return "America/Chicago"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="medium-12 small-12 columns"]//a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="medium-12 small-12 columns"]/h1/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="medium-12 small-12 columns"]//p//text()').getall())

    def get_images(self, response) -> list:
        return response.xpath('div[@class="medium-12 small-12 columns"]//img/@src').getall()
    
    def date_format(self) -> str:
        return "%m-%d-%Y"
    
    def get_date(self, response) -> Optional[str]:
        date_str = response.xpath('//div[@class="medium-8 small-12 columns"]//div[@class="medium-12 small-12 columns"]/p[1]/text()').get()
        date_str = date_str.strip()
        date_obj = datetime.strptime(date_str, "%B %d, %Y")
        return date_obj.strftime("%m-%d-%Y")  
        
    def get_authors(self, response):
        return []
     
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        # No Next page is there
        return None