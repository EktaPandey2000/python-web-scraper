from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class ConnecticutOfficeOfAttorneyGeneral(OCSpider):
    name = 'ConnecticutOfficeOfAttorneyGeneral'
    
    country = "US" 

    start_urls_names = {
        'https://portal.ct.gov/ag/press-releases': 'News'
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
        return response.xpath('//ul[@class= "list--desc"]//li//a/@href').getall() 
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//div[@class="content"]//h3[2]//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="content"]//text()').getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%m/%d/%Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//p[@class='date']/text()").re_first(r"(\d{1,2}/\d{1,2}/\d{4})")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        next_page = response.xpath("//a[contains(text(), 'Next')]/@href").get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None