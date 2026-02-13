from datetime import datetime
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
import logging
import re
from typing import Union
import scrapy
import json
import re

class OklahomaAttorneyGeneral(OCSpider):
    name = 'OklahomaAttorneyGeneral'

    country="US"
    
    custom_settings = {
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter',
    }
    
    HEADLESS_BROWSER_WAIT_TIME = 10000
    
    start_urls_names = {
        'https://oklahoma.gov/oag/news/newsroom.html': "News Releases", 
        'https://oklahoma.gov/oag/opinions/ag-opinions.html': "AG Opinions",
    }

    api_start_url = {
        'https://oklahoma.gov/oag/news/newsroom.html': {
            'url': 'https://oklahoma.gov/content/sok-wcm/en/oag/news/newsroom/jcr:content/responsivegrid-second/newslisting.json?page={page}&q=',
            'payload': {
                "page":'1',
                "q":''
            }
        },
        'https://oklahoma.gov/oag/opinions/ag-opinions.html': {
            'url': 'https://oklahoma.gov/content/sok-wcm/en/oag/opinions/ag-opinions/jcr:content/responsivegrid-second/container_2065963078/newslisting_copy.json',
            'payload': {
                "page":'1',
                "q":''
            }
        },
    }
    
    def parse_intermediate(self, response):
        start_url = response.meta.get('start_url')
        api_data = self.api_start_url[start_url]
        api_url = api_data["url"]
        if not api_url:
            self.logger.error(f"No API configuration found for start_url: {start_url}")
            return
        else:
            current_page = response.meta.get("current_page", 1)
            api_data["payload"]["page"] = str(current_page)
            api_url=api_url.format(page=current_page)
            payload = api_data["payload"]
            headers = {
                "Content-Type": "application/json"
            }
            yield scrapy.Request(
                url=api_url,
                method="GET",
                headers=headers,
                dont_filter=True,
                callback=self.parse,
                meta={
                    "start_url": start_url,
                    "api_url": api_url,
                    "payload": payload,
                    "current_page": current_page
                },
            )
            
    charset = "utf-8"
        
    @property
    def source_type(self) -> str:
        return "Ministry"
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "America/Chicago"
    
    def get_articles(self, response):
        matches = re.findall(r'\{.*\}', response.text, re.DOTALL)
        json_data = json.loads(matches[0]) if matches else {}       
        return [url["newsUrl"] for url in json_data["items"]] 
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath("//*[@class='title']//h1//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//*[@class='sok-container']//p//text()").getall()) 
    
    def get_images(self, response) -> list[str]:
        return []

    def get_authors(self, response):
        return []
    
    def get_document_urls(self, response, entry=None):
        return response.xpath("//*[@class='sok-container']//a[contains(@class,'cmp-button') or contains(text(),'full')]//@href").getall()

    def date_format(self) -> str:
        return "%Y-%m-%d"
    
    def get_date(self, response) -> str:
        date_text = response.xpath('//*[@aria-label="created-date"]//span//text()').get()
        cleaned_date_text = re.sub(r'^\w+, ', '', date_text)  # Extracted date from text
        try:
            parsed_date = datetime.strptime(cleaned_date_text, "%B %d, %Y").date()
            return parsed_date.strftime("%Y-%m-%d") 
        except ValueError:
            return ""  
        
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response, current_page) -> Union[None, str]:
        matches = re.findall(r'\{.*\}', response.text, re.DOTALL)
        json_data = json.loads(matches[0]) if matches else {}  
        return int(current_page)+1 if json_data["totalCount"] > current_page else None
    
    def go_to_next_page(self, response, start_url, current_page = 1):
        api_url = response.meta.get("api_url")
        if not api_url: 
            logging.info("API URL not found in meta data.")
            return
        next_page = self.get_next_page(response, current_page)
        if next_page:
            yield scrapy.Request(
                url=api_url,
                callback=self.parse_intermediate,
                meta={'current_page': next_page, 'start_url': start_url}
            )
        else:
            yield None 