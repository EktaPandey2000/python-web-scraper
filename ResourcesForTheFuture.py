from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class ResourcesForTheFuture(OCSpider):
    name = 'ResourcesForTheFuture'
    
    country = "US"

    HEADLESS_BROWSER_WAIT_TIME = 10000  # 10 seconds wait time

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.HeadlessBrowserProxy': 350
            },
        "DOWNLOAD_DELAY": 1
    }

    start_urls_names = {
        'https://www.rff.org/news/all-news/': 'News',
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
        return response.xpath('//a[contains(@class, "card--link")]/@href').getall()
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="hero__title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date = response.xpath('normalize-space(//p[@class="hero-meta__column-content"]/text())').get()
        if not date:
            return ""
        try:
            dt = datetime.strptime(date, "%B %d, %Y")
        except ValueError:
            try:
                dt = datetime.strptime(date, "%b. %d, %Y")
            except ValueError:
                return "" 
        return dt.strftime(self.date_format())

    def get_authors(self, response):
        return ""

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        if not response.xpath('//a[contains(@class, "card--link")]'):
            return None
        current_url = response.url
        if "offset=" in current_url:
            current_offset = int(current_url.split("offset=")[-1])
        else:
            current_offset = 0
        next_offset = current_offset + 12  
        return f"https://www.rff.org/news/all-news/?offset={next_offset}"