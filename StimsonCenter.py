from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class StimsonCenter(OCSpider):
    name = "StimsonCenter"
    
    country = "US"

    start_urls_names = {
        "https://www.stimson.org/about/stimson/media-announcements/" : "Newsroom"
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
        return "US/Eastern"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@data-elementor-id="66429"]/div[1]/div[2]//a/@href').getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//h1[@class="elementor-heading-title elementor-size-default"]//text()').get()
        
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="elementor-widget-container"]//p/text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//time/text()').get()
        
    def get_authors(self, response):
        return ""
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response): 
        # No next page to scrape
        return None