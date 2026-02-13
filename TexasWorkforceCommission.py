from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class TexasWorkforceCommission(OCSpider):
    name = 'TexasWorkforceCommission'
    
    country = "US"

    start_urls_names = {
        'https://www.twc.texas.gov/news': 'News'
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
        return response.xpath('//span[@class= "field-content"]//a/@href').getall() 
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        title = response.xpath('//h1[@class= "news-title"]/span/text()').get()
        return title
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class= "news_body"]//p//text()').getall())
    
    def get_images(self, response) -> list[str]:
        return [] 
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//div[@class= "news_date"]/text()').re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return []

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        next_page = response.xpath("//a[contains(@class, 'usa-pagination__next-page')]/@href").get()
        if next_page:
            return next_page
        else:
            return None