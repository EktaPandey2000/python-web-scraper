from datetime import datetime 
import re
import scrapy
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class MinnesotaDepartmentOfTransportation(OCSpider):
    name = 'MinnesotaDepartmentOfTransportation'
    
    country = "US"

    start_urls_names = {
        'https://www.dot.state.mn.us/news/index.html': 'News'
    }
    
    def parse_intermediate(self, response):
        articles = response.xpath('//div[contains(@class, "targetDiv")]//a/@href').getall()
        total_articles = len(articles)
        start_url = response.meta.get("start_url")
        for start_idx in range(0, total_articles, 100):
            yield scrapy.Request(
                    url=start_url,
                    callback=self.parse,
                    meta={
                        'start_idx': start_idx, 
                        'start_url': start_url
                    },
                    dont_filter=True
            )
    
    charset = "utf-8"

    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Central"
    
    def get_articles(self, response) -> list:
        articles = response.xpath('//div[contains(@class, "targetDiv")]//a/@href').getall()
        unique_articles = list(set(articles)) 
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100
        return unique_articles[start_idx:end_idx]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h2//text() | //h3//text()').get() 
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//section[@class ="side-main-content"]//article//text()').getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"   

    def get_date(self, response) -> str:
        date_str = response.xpath('//div[@id="page-title"]/p//text()').get(default='').strip()
        date_str = re.sub(r'([A-Za-z]{3})[a-z.]*', r'\1', date_str)
        date_formats = ["%b %d, %Y"]
        for fmt in date_formats:
            try:
                parsed_date = datetime.strptime(date_str, fmt)
                return parsed_date.strftime("%B %d, %Y")
            except ValueError:
                continue
        return ""

    def get_authors(self, response):
        return []

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        # No next page is there to scrap
        return None