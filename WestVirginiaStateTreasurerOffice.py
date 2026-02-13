from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class WestVirginiaStateTreasurerOffice(OCSpider):
    name = "WestVirginiaStateTreasurerOffice"

    country="US"

    start_urls_names = {
        "https://wvsto.com/About/Press-Releases": "Press Releases",
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
        return "America/New_York"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="app-news5-details-link"]//a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="app-news5-content"]//h2/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="app-news5-content"]//h2/text()' ).getall())

    def get_images(self, response) -> list:
        return response.xpath('//div[@class="app-news5-detail-img"]//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m/%d/%Y"
    
    def get_date(self, response) -> Optional[str]:
        return response.xpath('//div[@class="app-news5-content"]/span[@class="app-news5-date "]/text()').re_first(r"\b\d{1,2}[//]\d{1,2}[//]\d{4}\b")
           
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//ul[@class="pagination justify-content-center"]/li[last()]/a[@class="page-link"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None