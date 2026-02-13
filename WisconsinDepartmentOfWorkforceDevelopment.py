from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class WisconsinDepartmentOfWorkforceDevelopment(OCSpider):
    name = "WisconsinDepartmentOfWorkforceDevelopment"

    country = "US"

    start_urls_names = {
        "https://dwd.wisconsin.gov/news/stories/": "News",
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
        return response.xpath("//div[@class='news-content']/h2/a[contains(@href,'/news/')]//@href").getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> Optional[str]:
        return response.xpath("//h1[@class='text-center blk-txt mt-4']/text() | //h1[@class='mb-1']/text() | //h1/text() | //title/text()").get()

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@id="content-wrapper"]//p[not(ancestor::figure)]').getall())

    def get_images(self, response) -> list:
        return response.xpath('//figure[@class="figure"]//img/@src').getall()

    def date_format(self) -> str:
        return "%m/%d/%Y"

    def get_date(self, response) -> Optional[str]:
        date_str = response.xpath(
            '//div[contains(@class, "col-12 col-sm-8")]//p//text()[2] | '
            '//div[contains(@class, "row") and contains(@class, "mb-3")]//p/em/text()'
        ).re_first(r"\b[A-Za-z]{3,9}\.? \d{1,2}, \d{4}\b")
        if date_str:
            date_str = date_str.replace(".","") 
            for fmt in ["%b %d, %Y", "%B %d, %Y"]:
                try:
                    date_obj = datetime.strptime(date_str, fmt)
                    return date_obj.strftime(self.date_format())
                except ValueError:
                    continue

    def get_authors(self, response):
        return ""
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) -> Optional[str]: 
       # No next page to scrape
       return None