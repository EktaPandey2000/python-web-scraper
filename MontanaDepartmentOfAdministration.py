from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
import scrapy
import json
import re

class MontanaDepartmentOfAdministration(OCSpider):
    name = 'MontanaDepartmentOfAdministration'
    
    country = "US"

    start_urls_names = {
        'https://news.mt.gov/Department-of-Administration/': 'Montana'
    }
    
    api_start_url = {
        'https://news.mt.gov/Department-of-Administration/':'https://news.mt.gov/Department-of-Administration/articles.json?_=1739942362939'
    }
    
    def parse_intermediate(self, response):
        start_url = response.meta.get("start_url")
        api_url = self.api_start_url.get(start_url)
        if not api_url:
            self.logger.error(f"No API configuration found for start_url: {start_url}")
        else:
            self.logger.info(f"Fetching API URL: {api_url}")
        yield scrapy.Request(
            url=api_url,
            callback=self.parse,
            meta={
                "start_url": start_url,
                "api_url": api_url
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
    def timezone(self):
        return "US/Mountain"
    
    def get_articles(self, response) -> list:
        data = json.loads(response.text)
        links = [item["link"] for item in data if "link" in item]
        return links
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//div[@class="col-lg-8 order-1 order-lg-0"]//h1//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='col-lg-8 order-1 order-lg-0']//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d %Y" 

    def get_date(self, response) -> str:
        date_str = response.xpath("//ul[@class='meta list-inline text-muted']//li[@class='date']//text()").get()
        if date_str:
            date_str = re.sub(r"\s+", " ", date_str.strip()) 
            return re.search(r"([A-Za-z]+ \d{1,2} \d{4})", date_str).group(1) if re.search(r"([A-Za-z]+ \d{1,2} \d{4})", date_str) else None
        else:
            return None

    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        # No next page to scrap
        return None