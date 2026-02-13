from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 
import scrapy

class UtahDepartmentOfWorkforceServices(OCSpider):
    name = "UtahDepartmentOfWorkforceServices"

    country = "US"

    start_urls_names = {
        "https://jobs.utah.gov/department/press.html": "Press Release"
    }

    proxy_country = "us"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.GeoProxyMiddleware': 350,
            },
        "DOWNLOAD_DELAY": 2,
    }

    charset = "utf-8"

    def parse_intermediate(self, response):
        all_articles = list(set(response.xpath('//ul/li/a[starts-with(@href, "/department/press")]/@href').getall()))
        total_articles = len(all_articles)
        articles_per_page = 100
        start_url = response.meta.get("start_url", response.url)
        for start_idx in range(0, total_articles, articles_per_page):
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                meta={
                    'start_idx': start_idx, 
                    'articles': all_articles, 
                    'start_url': start_url
                },
                dont_filter=True
            )

    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def language(self): 
        return "English"
    
    @property
    def timezone(self):
        return "America/Denver"
    
    def get_articles(self, response) -> list:
        all_articles = response.meta.get('articles', [])
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100
        return all_articles[start_idx:end_idx]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        title =response.xpath('//h2//text()').get()
        if title:
            return title
        return response.xpath("//div[@class='col-md-9']//p[1]//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='col-md-12']//p//text()").getall())

    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return"%m/%d/%Y"
    
    def get_date(self, response) -> str:
        return datetime.strptime(response.xpath('//h1/br/following-sibling::text()').get().strip(), "%B %d, %Y").strftime("%m/%d/%Y")
    
    def get_authors(self, response):
        return ""
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        # No next page to scrape
        return None