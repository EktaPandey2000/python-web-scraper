from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime
import urllib.parse
import scrapy

class SouthCarolinaAttorneyGeneral(OCSpider):
    name = "SouthCarolinaAttorneyGeneral"

    country = "US"

    start_urls_names = {
        "https://www.scag.gov/about-the-office/news/": "Latest News",
    }
    
    api_start_urls = {
        "https://www.scag.gov/about-the-office/news/": {
            "url": "https://www.scag.gov/about-the-office/news/",
            "payload": {
                      "page": "1",
            }
        }
    }

    custom_settings = {
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter',
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
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
    
    def parse_intermediate(self, response):
        start_url = response.meta.get("start_url")
        api_data = self.api_start_urls.get(start_url)
        if not api_data:
            return
        payload = response.meta.get("payload", api_data["payload"].copy())
        api_url = api_data["url"]
        full_api_url = f"{api_url}?{urllib.parse.urlencode(payload)}"
        yield scrapy.Request(
            url=full_api_url,
            method="GET",
            headers=self.headers,
            callback=self.parse,
            meta={
                "start_url": start_url,
                "api_url": api_url,
                "payload": payload,
                "current_page": payload["page"]
            }
        )

    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="news-card h-100"]/a/@href').getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="col-lg-8"]/h1/text()').get()

    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="col-lg-8"]/div//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        date_str = response.xpath('//div[@class="col-lg-8"]/p[@class="date"]/text()').get()
        return datetime.strptime(date_str, "%b %d, %Y").strftime("%m-%d-%Y") 
        
    def get_authors(self, response):
        return []
    
    def get_next_page(self, response, current_page: Optional[int] = 1) -> Optional[int]:
        next_page = int(current_page) + 1
        return next_page

    def get_page_flag(self) -> bool:
        return False
    
    def go_to_next_page(self, response, start_url, current_page: Optional[int] = 1):
        api_data = self.api_start_urls.get(start_url)
        api_url = api_data["url"]
        payload = response.meta.get("payload", {}).copy()
        next_page = self.get_next_page(response, current_page)
        payload["page"] = next_page  
        full_api_url = f"{api_url}?page={payload['page']}"
        yield scrapy.Request(
            url=full_api_url,
            method="GET",
            headers=self.headers,
            callback=self.parse_intermediate,
            meta={
                "start_url": start_url,
                "api_url": api_url,
                "payload": payload,
                "current_page": next_page
            },    
        )      