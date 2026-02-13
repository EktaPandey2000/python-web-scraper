from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class TennesseeAttorneyGeneral(OCSpider):
    name = "TennesseeAttorneyGeneral"

    country = "US"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350
        },
        "DOWNLOAD_DELAY": 5,
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter',
    }

    HEADLESS_BROWSER_WAIT_TIME = 30000  # 30 Seconds wait time

    start_urls_names = {
        "https://www.tn.gov/attorneygeneral/news.html": "Newsroom",
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
        return "America/New_York"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="tn-newsroomresults"]//ul[@class="stories active"]//li//article//h2/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="tn-pagetitle show"]//h1/text()').get()

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="tn-rte"]//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return response.xpath('//div[@class="content"]//article//p//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        Raw_date = (response.xpath('normalize-space(//div[@class="date"]/text())').get() or "").strip()
        date_str = Raw_date.split("|")[0].strip()
        date_obj = datetime.strptime(date_str, "%A, %B %d, %Y")
        return date_obj.strftime("%m-%d-%Y")
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//ul[@class="inline-list pager"]//a[@aria-label="Next Page"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None