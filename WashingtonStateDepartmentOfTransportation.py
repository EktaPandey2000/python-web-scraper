from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class WashingtonStateDepartmentOfTransportation(OCSpider):
    name = "WashingtonStateDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://wsdot.wa.gov/about/news": "News"
    }

    charset="utf-8"

    @property
    def language(self) -> str:
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self) -> str:
        return "US/Eastern"
    
    def get_articles(self, response) :
        return response.xpath('//div[@class="newsContent"]//a/@href').getall()
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) :
        return response.xpath('//h1[@class="page-header"]/span//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="content"]//p//text()').getall())

    def get_images(self, response) :
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        return response.xpath('//time/text()').get()
    
    def get_authors(self, response) :
        return []
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) :
        return response.xpath('//a[@title="Go to next page"]/@href').get()