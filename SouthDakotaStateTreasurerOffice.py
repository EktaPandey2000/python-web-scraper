from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class SouthDakotaStateTreasurerOffice(OCSpider):
    name = "SouthDakotaStateTreasurerOffice"

    country="US"

    start_urls_names = {
        "https://dor.sd.gov/newsroom/": "Newsroom",
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
        return response.xpath('//div[@class="card-body"]/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="headline__text"]/h1/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="article__body"]//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return response.xpath('//div[@class="heading__image"]//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//div[@class="headline__date-read"]//time/text()').re_first(r"\d{2}-\d{2}-\d{4}")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//li[@class="page-item page-item--next"]/a/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None