from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class TexasAttorneyGeneral(OCSpider):
    name = "TexasAttorneyGeneral"
    
    country = "US"
   
    start_urls_names = {
        "https://www.texasattorneygeneral.gov/news/releases": "News Releases",
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
        return "America/Chicago"
    
    def get_articles(self, response) -> list:
        return response.xpath('//h4[@class="m-b-1 h4-sans"]/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('normalize-space(//div[@class="cell small-24 medium-20 large-18"]/h1)').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="main-content-wysiwyg-container"]//p//text()').getall())

    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%m-%d-%Y"
    
    def get_date(self, response):
        date_str = response.xpath('//div[@class="meta m-t-3 m-b-2"]/text()[1]').get()
        clean_date = " ".join(date_str.strip().split('|')[0].split())  # Extracted date from full text
        return datetime.strptime(clean_date, "%B %d, %Y").strftime("%m-%d-%Y")
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//div[@class="cell small-6 medium-4 text-right pager__item pager__item--next"]/a[@title="Go to next page"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None