from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class FloridaOfficeOfAttorneyGeneral(OCSpider):
    name = 'FloridaOfficeOfAttorneyGeneral'
    
    country = "US"
    
    start_urls_names = {
        'https://www.myfloridalegal.com/newsreleases': 'News Releases',
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
    
    def get_articles(self, response) -> list:
        return response.xpath("//td[@class='views-field views-field-title']//a/@href").getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath("//h1[@class= 'main_heading1 animated fadeIn']//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='field field--name-body field--type-text-with-summary field--label-hidden field__item']//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%b %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//*[@id='block-my-florida-legal-content']/div/div[2]/div[2]//text()").re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath("//li[@class='pager__item pager__item--next']//a/@href").get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None