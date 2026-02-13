from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class TennesseeDepartmentOfTransportation(OCSpider):
    name = "TennesseeDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://www.tn.gov/tdot/news.html": "News"
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
        return response.xpath('//div[@class="padded"]//a/@href').getall()
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) :
        return response.xpath('//div[@class="tn-pagetitle show"]/h1//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="tn-rte"]//p//text()').getall())

    def get_images(self, response) :
        return []

    def date_format(self) -> str:
        return "%A, %B %d, %Y"

    def get_date(self, response) -> str:
        return response.xpath('//div[@class="date"]//text()').get().replace("|", "").strip()
    
    def get_authors(self, response) :
        return []
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) :
        return response.xpath('//a[@title="Next Page"]/@href').get()