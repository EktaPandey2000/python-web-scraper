from scraper.utils.helper import body_normalization
from scraper.OCSpider import OCSpider
import json
import logging
from typing import List, Optional
import scrapy
import urllib

class MichiganDepartmentOfTreasury(OCSpider):
    name = "MichiganDepartmentOfTreasury"
    
    country = "US"
    
    start_urls_names = {
        'https://www.michigan.gov/treasury/news': "News"
    }
    
    api_start_urls = {
        "https://www.michigan.gov/treasury/news": "https://www.michigan.gov/treasury/sxa/search/results/?s={62E9FB6A-7717-4EF1-832C-E5ECBB9BB2D9}&itemid={476B9252-7096-4672-8149-A1B6B92FAD61}&sig=&autoFireSearch=true&v=%7BB7A22BE8-17FC-44A5-83BC-F54442A57941%7D&p=10&o=Article%20Date%2CDescending"
    }

    def parse_intermediate(self, response):
        start_url = response.meta.get("start_url")
        api_base_url = self.api_start_urls.get(start_url)
        current_page = response.meta.get("current_page", 1)
        if not api_base_url:
            self.logger.error(f"No API configuration found for start_url: {start_url}")
            return
        payload = response.meta.get("payload", {"e": 0})
        encoded_payload = urllib.parse.urlencode(payload) 
        api_url = f"{api_base_url}&{encoded_payload}"  
        yield scrapy.Request(
            url=api_url,
            method="GET",
            callback=self.parse,
            meta={
                "start_url": start_url,
                "api_url": api_base_url,
                "payload": payload,
                "current_page": current_page 
            },
        )
        
    charset = "utf-8"
        
    @property
    def language(self):
        return "English"

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self) -> str:
        return "US/Eastern"

    def get_articles(self, response) -> List[str]:
        try:
            data = json.loads(response.text)
            articles = data.get("Results", [])
            return [article.get("Url") for article in articles if article]
        except json.JSONDecodeError as e:
            self.logger.error(f"Error decoding JSON: {e}")
            return []

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> Optional[str]:
        return response.xpath("//h1/text()").get()
        
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='news-item__section-content']//p//text()").getall())

    def get_images(self, response) -> List[str]:
        return response.xpath("//@style").re(r"url\((.*?)\)")

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> Optional[str]:
        return response.xpath("//div[@class='news-item__section-date']/p/text()").re_first(r"\w+\s\d{1,2},\s\d{4}")

    def get_authors(self, response) -> List[str]:
        return []

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response, current_page) -> Optional[int]:
        payload = response.meta.get("payload", {})
        data = response.json()
        current_page = response.meta.get("current_page", 1)
        current_e = int(payload.get("e", 0))
        new_e = current_e + 10
        count = data.get("Count")
        if new_e >= count:
            return None
        else:
            return current_page + 1
        
    def go_to_next_page(self, response, start_url, current_page):
        api_url = response.meta.get("api_url")
        payload = response.meta.get("payload", {})
        if not api_url:
            logging.error("API URL not found in meta data.")
            return
        next_page = self.get_next_page(response, current_page)
        if next_page:
            current_e = int(payload.get("e", 0))
            new_e = current_e + 10
            payload["e"] = new_e 
            yield scrapy.Request(
                url=f"{api_url}&e={new_e}",
                method='GET',
                callback=self.parse_intermediate,
                meta={
                    "start_url": start_url,
                    "api_url": api_url,
                    "payload": payload,
                    "current_page": next_page
                },
                dont_filter=True
            )
        else:
            logging.info("No more pages to fetch.")