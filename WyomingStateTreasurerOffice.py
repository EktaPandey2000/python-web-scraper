from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class WyomingStateTreasurerOffice(OCSpider):
    name = "WyomingStateTreasurerOffice"
    
    country = "US"
    
    start_urls_names = {
        "https://statetreasurer.wyo.gov/2025/01/": "News",
    }
    
    charset = "utf-8"
    
    visited_links = set()  # Keep track of visited URLs to avoid reprocessing

    @property
    def language(self): 
        return "English"
     
    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def timezone(self):
        return "America/Denver"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="container"]//h2[@class="entry-title"]/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="et_pb_title_container"]/h1[@class="entry-title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="et_pb_text_inner"]/p/text()').getall())

    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> Optional[str]:
        date_str = response.xpath('//div[@class="et_pb_title_container"]//p/span/text()').get()
        date_str = date_str.strip()  
        date_obj = datetime.strptime(date_str, "%b %d, %Y")
        return date_obj.strftime("%m-%d-%Y")
       
    def get_authors(self, response):
        return []
    
    def get_document_urls(self, response, entry=None) -> list:
        return response.xpath('//div[@class="et_pb_text_inner"]//a[contains(@href, ".pdf")]/@href').getall()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        # Extract all archive links
        next_pages = response.xpath('//div[@id="archives-2"]//li/a/@href').getall()
        filtered_pages = next_pages[2:]
        for next_page in filtered_pages:
            if next_page not in self.visited_links:
                self.visited_links.add(next_page)
                return next_page 
        return None