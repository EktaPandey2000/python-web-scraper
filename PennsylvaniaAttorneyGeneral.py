from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class PennsylvaniaAttorneyGeneral(OCSpider):
    name = "PennsylvaniaAttorneyGeneral"

    country = "US"

    start_urls_names = {
        "https://www.attorneygeneral.gov/taking-action/": "News: Taking Action Items",
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
        return "America/New_York"
    
    def get_articles(self, response) -> list:
        return response.xpath('//table[@class="table table-striped stories"]//td[@class="title"]/a/@href').getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="breadcrumb ml-0 pl-0"]//span[last()]/span[@property="name"]/text()').get()

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="col-md-8 pt-3"]//p[not(@align)]/text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        date_str = response.xpath('//div[@class="col-md-12 meta mt-md-2"]/span/text()').get()
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%m-%d-%Y") 
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//div[@class="page-links float-right"]//a[@class="next page-numbers"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None