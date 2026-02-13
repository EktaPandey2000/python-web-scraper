from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class WashingtonStateTreasurerOffice(OCSpider):
    name = "WashingtonStateTreasurerOffice"

    country="US"

    start_urls_names = {
        "https://tre.wa.gov/about-us/media-center": "Media Center",
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
        return "America/Los_Angeles"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="views-field views-field-title"]//a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="content"]//h1[@class="title"]//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath(
        '//div[@class="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"]' ).getall())

    def get_images(self, response) -> list:
        return response.xpath('//div[@class="app-news5-detail-img"]//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> Optional[str]:
        date_str = response.xpath('//div[@class="field field--name-field-date field--type-datetime field--label-hidden my-5"]/time/text()').get()
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%m-%d-%Y") 
       
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//nav[@class="mt-5"]//ul[@class="pagination js-pager__items"]//li[@class="page-item active"]/following-sibling::li[1]/a/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None