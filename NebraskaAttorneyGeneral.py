from scraper.utils.helper import body_normalization
from scraper.OCSpider import OCSpider
import scrapy

class NebraskaAttorneyGeneral(OCSpider):
    name = 'NebraskaAttorneyGeneral'

    country = "US"

    start_urls_names = {
        "https://ago.nebraska.gov/archived-news":"News",
    }

    def parse_intermediate(self, response):
        all_articles = list(set(response.xpath("//div[@class='view-content']//a/@href").getall()))
        total_articles = len(all_articles)
        articles_per_page = 100
        start_url = response.meta.get("start_url", response.url)
        # Have more than 100 articles on start URL
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
    def language(self):
        return "English"

    @property
    def source_type(self) -> str:
        return 'ministry'
    
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
        return response.xpath("//h1[@class='page-header']//span//text()").get()
        
    def get_body(self, response) -> str:
        body = body_normalization(response.xpath("//div[@class='field field--name-body field--type-text-with-summary field--label-hidden field--item']//div//text() | //div[@class='field field--name-body field--type-text-with-summary field--label-hidden field--item']//p//text()").getall())
        return body
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%A, %B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//div[@class='field field--name-field-post-date field--type-datetime field--label-inline']//div[@class='field--item']//text()").get()
    
    def get_authors(self, response):
        return []
    
    def get_document_urls(self, response, entry=None):
        return response.xpath("//a[contains(@href,'.pdf')]//@href").getall()
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        return None