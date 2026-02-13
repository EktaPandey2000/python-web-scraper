from datetime import datetime
import re
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class DelawareAttorneyGeneral(OCSpider):
    name = 'DelawareAttorneyGeneral'
    
    country = "US"

    start_urls_names = {
        'https://news.delaware.gov/category/justice/': 'News'
    }
    
    custom_settings = {
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter'
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
    
    def get_articles(self, response) -> list:
        return response.xpath("//div[@id = 'main_content']//h3/a/@href").getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath("//header[@class='pull-left']//h1/text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//*[@id='main_content']/div/p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B, %d, %Y"
    
    def get_date(self, response):
        raw_date_text = response.xpath("//*[@id='main_header']/div/header//p[@class='text-muted small']/text()[contains(., 'Date Posted')]").get()
        if raw_date_text:
            match = re.search(r"Date Posted:\s*(?:\w+, )?(\w+ \d{1,2}, \d{4})", raw_date_text)
            if match:
                extracted_date = match.group(1)
                # Convert to datetime object and format
                formatted_date = datetime.strptime(extracted_date, "%B %d, %Y").strftime("%B, %d, %Y")
                return formatted_date
        return None    
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        next_page = response.xpath('//div[@class="pagination"]//a[@class="btn btn-default btn-sm" and span[contains(text(), "Go to next page")]]/@href').get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None