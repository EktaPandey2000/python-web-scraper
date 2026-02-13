from datetime import datetime
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class ColoradoDepartmentOfTheTreasury(OCSpider):
    name = "ColoradoDepartmentOfTheTreasury"

    country="US"

    start_urls_names = {
        "https://treasury.colorado.gov/category/press-release":"Press Release",
    }

    charset = "utf-8"

    @property
    def source_type(self) -> str:
        return 'ministry'
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Mountain"
    
    def get_articles(self, response) -> list:
       return response.xpath('//*[@id="main-content"]//*[@class="node-readmore"]//a//@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//*[@id="main-content"]//h1//text()').get()
       
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="region region-content"]//p//text()').getall())
    
    def get_images(self, response, entry=None) :
        return response.xpath('//div[@class="region region-content"]//img/@src').getall()

    def date_format(self) -> str:
        return "%Y.%m.%d"
    
    def get_date(self, response) -> str:
        date_text = response.xpath('//div[@class="region region-content"]//time/@title').get()
        if date_text:
            date_obj = datetime.strptime(date_text, '%A, %B %d, %Y - %I:%M %p')
            formatted_date = date_obj.strftime("%Y.%m.%d")
            return formatted_date
        
    def get_authors(self, response, entry=None) -> list[str]:
        return []

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        return response.xpath('//*[@id="main-content"]//a[@rel="next"]/@href').get()