from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class WisconsinEconomicDevelopmentCorporation(OCSpider):
    name = 'WisconsinEconomicDevelopmentCorporation'
    
    country = "US"

    start_urls_names = {
        'https://wedc.org/newsroom/': 'News'
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
        return "US/Central"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class= "fusion-post-content post-content"]/h4/a/@href').getall() 
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class= "fusion-content-tb fusion-content-tb-1 success-story-content"]//p/text()').getall())
    
    def get_images(self, response) -> list[str]:
        return response.xpath('//div[@class= "fusion-text fusion-text-13"]/p/img/@src').getall()
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//span[@class= "fusion-tb-published-date"]/text()').re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return ""
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        next_page = response.xpath('//a[@class= "pagination-next"]/@href').get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None