from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class GeorgiaAttorneyGeneral(OCSpider):
    name = "GeorgiaAttorneyGeneral"

    country = "US"

    start_urls_names = {
        "https://law.georgia.gov/press-releases": "News Releases",
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
        return response.xpath('//div[@class="contextual-region news-teaser"]//a/@href').getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        title = response.xpath('//div[@class="heading-lockup__title-wrapper"]/h1/text()').get().strip()
        return title

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//main[@class="content-page__main"]//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        date_str = (response.xpath('//div[@class="heading-lockup__title-wrapper"]/p[@class="heading-lockup__label"]/text()').get()).strip()
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%m-%d-%Y") 
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//li[@class="pager__item pager__item--next"]/a/@href').get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None