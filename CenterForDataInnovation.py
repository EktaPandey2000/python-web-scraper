from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class CenterForDataInnovation(OCSpider):
    name = 'CenterForDataInnovation'
    
    country = "US"

    start_urls_names = {
        'https://datainnovation.org/category/press-release/': 'Press Release'
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
    
    def get_articles(self, response) :
        return response.xpath('//h2[@class="penci-entry-title entry-title grid-title"]/a/@href').getall()
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="post-title single-post-title entry-title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date_str = response.xpath('normalize-space(//time[@class="entry-date published"]/text())').get()
        if date_str:
            try:
                dt = datetime.strptime(date_str, self.date_format())
                return dt.strftime(self.date_format())
            except ValueError:
                pass
        else:    
            return ""

    def get_authors(self, response):
        return response.xpath('//a[@class="author url fn" and @rel="author"]/text()').get()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath("//div[@class='older']/a/@href").get()
        if next_page:
            return next_page
        else:
            return None