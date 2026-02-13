from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class BelferCenterForScienceAndInternationalAffairs(OCSpider):
    name = 'BelferCenterForScienceAndInternationalAffairs'
    
    country = "US"

    start_urls_names = {
        'https://www.belfercenter.org/latest': 'Press Release'  # Pagination is not supported
    }

    start_urls_with_no_pagination_set = {
        'https://www.belfercenter.org/latest'
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
        return list(set(response.xpath("//a[starts-with(@href, '/') and @class='card-link js-link-event-link']/@href").getall()))
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="h4"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date_str = response.xpath('normalize-space(//time[@class="datetime"]/text())').get()
        if date_str:
            try:
                date_str_clean = date_str.replace('.', '')
                dt = datetime.strptime(date_str_clean, "%b %d, %Y")
                return dt.strftime(self.date_format())
            except ValueError:
                pass
        else:    
            return ""

    def get_authors(self, response):
        return response.xpath('//a[@class="js-link-event-link"]/text()').get()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        # No next page to scrape
        return None