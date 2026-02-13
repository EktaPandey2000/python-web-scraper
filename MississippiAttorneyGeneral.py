from scraper.OCSpider import OCSpider
from typing import List
import scrapy
import re

class MississippiAttorneyGeneral(OCSpider):
    name = 'MississippiAttorneyGeneral'

    country = "US"
    
    start_urls_names = {
        'https://attorneygenerallynnfitch.com/media/press-releases/': "Press Releases"
    }

    def parse_intermediate(self, response):
        all_articles = list(set(response.xpath("//div[@id='_dynamic_list-75-65']//span//a//@href").getall()))
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
    def timezone(self):
        return "US/Central"

    @property
    def language(self):
        return "English"

    def get_articles(self, response) -> list:
        all_articles = response.meta.get('articles', [])
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100
        return all_articles[start_idx:end_idx]

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        text = response.xpath("//div[@class='ct-section-inner-wrap']//h1//span//text()").get()
        title_parts = text.split('(', 1)
        return title_parts[0].strip() if len(title_parts) > 1 else text.strip()

    def get_body(self, response) -> str:
        # Only PDF's are there to scrape
        return ""
    
    def get_images(self, response) -> list:
        # Only PDF's are there to scrape
        return []

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        match = re.search(r"/(\d{4})/(\d{2})/(\d{2})/", response.url)
        if match:
            year, month, day = match.groups()
            return f"{year}-{month}-{day}"
        return None

    def get_authors(self, response):
        # Only PDF's are there to scrape
        return []
    
    def get_document_urls(self, response, entry=None) -> List[str]:
        return response.xpath("//div[@class='pdfjs-fullscreen']//a//@href").getall()

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No more pages to scrape
        return None