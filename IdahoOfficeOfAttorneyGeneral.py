from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class IdahoOfficeOfAttorneyGeneral(OCSpider):
    name = 'IdahoOfficeOfAttorneyGeneral'
    
    country = "US"
    
    start_urls_names = {
        'https://www.ag.idaho.gov/newsroom/category/press-releases/': 'Press Releases',
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
        return "US/Mountain"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="post-card-wrapper"]/article[@class= "post-card"]/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1//text()').get() 
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='entry-content']//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//div[@class='header-text-wrapper']//p[2]//text()").re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath("//a[div[contains(@class, 'nav-prev')]]/@href").get()
        if not next_page:
            next_page = response.xpath("//a[contains(text(), 'Older') or contains(div/text(), 'Older')]/@href").get()
        return next_page        