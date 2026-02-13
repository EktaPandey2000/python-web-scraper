from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from typing import List, Union
from datetime import datetime
import re

class NewJerseyDepartmentOfTreasury(OCSpider):
    name = "NewJerseyDepartmentOfTreasury"

    country = "US"
    
    charset = "utf-8"

    start_urls_names = {
        "https://www.nj.gov/treasury/news.shtml": "Treasury Press Releases"
    }

    @property
    def language(self) -> str:
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self) -> str:
        return "US/Eastern"
    
    def get_articles(self, response) -> List[str]:
        return response.xpath("//table[@id='example1']/tbody/tr/td/a/@href").getall()
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) -> Union[str, None]:
        return response.xpath("//div/p/strong/text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='row']//p/text()").getall()) 

    def get_images(self, response) -> List[str]:
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date_text = response.xpath("//div[@class='col-md-6']/strong/following-sibling::text()").get()
        return (match.group(1) if (date_text and (match := re.search(r"([A-Za-z]+ \d{1,2}, \d{4})", date_text.strip())))
        else datetime.today().strftime("%B %d, %Y"))
        
    def get_authors(self, response) -> List[str]:
        return []

    def get_document_urls(self, response, entry=None) -> List[str]:
        return response.xpath("//div[@class='col-md-12']//p//a/@href").getall()

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> Union[None, str]:
        # No next page to scrap
        return None 