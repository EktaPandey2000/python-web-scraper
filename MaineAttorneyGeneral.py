from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from typing import List
import scrapy

class MaineAttorneyGeneral(OCSpider):
    name = 'MaineAttorneyGeneral'

    country = "US"
    
    start_urls_names = {
        'https://www.maine.gov/ag/news/press_release_archive.shtml/': "Press Release"
    }

    def parse_intermediate(self, response):
        all_articles = list(set(response.xpath("//ul[@class='plain']//li//a//@href").getall()))
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
            
    charset = "utf-8"

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Central"

    def get_articles(self, response) -> list:
        all_articles = response.meta.get('articles', [])
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100
        return all_articles[start_idx:end_idx]

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return response.xpath("//h1//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@id='maincontent2']//p//text()").getall())
    
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return '%B %d, %Y'

    def get_date(self, response) -> str:
        return response.xpath("//div[@id='maincontent2']//p/text()").get()
    
    def get_authors(self, response):
        return []

    def get_document_urls(self, response, entry=None) -> List[str]:
        return response.xpath("//div[@id='maincontent2']//p//a[contains(@href,'php')]//@href").getall()

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No more pages to scrape
        return None