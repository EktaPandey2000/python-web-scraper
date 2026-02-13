from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class OregonAttorneyGeneral(OCSpider):
    name = "OregonAttorneyGeneral"

    country = "US"

    start_urls_names = {
        "https://www.doj.state.or.us/media/news-media-releases/oregon-doj-news/": "News Releases"
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
        return response.xpath('//div[@class="pure-u-1 results-item"]/h3/a/@href').getall()
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) :
        return response.xpath('//h1[@class="page-main-title"]/span/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//article[@id="post-54271"]//p/text()').getall())

    def get_images(self, response) :
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        return response.xpath('//div[@class="date"]//text()').get()
    
    def get_authors(self, response) :
        return []
    
    def get_document_urls(self, response, entry=None):
        return response.xpath('//article[@id="post-54271"]//p/a/@href').getall()
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) :
        return response.xpath('//div[@class="nav-previous"]//a/@href').get()   