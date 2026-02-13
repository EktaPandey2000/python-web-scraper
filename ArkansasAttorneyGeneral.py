import scrapy
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class ArkansasAttorneyGeneral(OCSpider):
    name = 'ArkansasAttorneyGeneral'
    
    country = "US"
    
    start_urls_names = {
        'https://arkansasag.gov/news-alerts/news-releases/': 'news releases',
    }
    
    def parse_intermediate(self, response):
        articles = response.xpath('//div[@class="dce-post-block"]//a//@href').getall()
        total_articles = len(articles)
        start_url = response.meta.get("start_url")
        # Have more than 100 articles on start URL
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
    def language(self):
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "US/Central"
    
    def get_articles(self, response) -> list:
        articles = response.xpath('//div[@class="dce-post-block"]//a//@href').getall()
        unique_articles = list(set(articles)) 
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100   # Have more than 100 articles on start URL
        return unique_articles[start_idx:end_idx]   
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class= "elementor-widget-container"]//h1//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class= 'elementor-element elementor-element-7f465e92 elementor-widget elementor-widget-theme-post-content']//p//text()").getall())
    
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//span[@class= 'elementor-icon-list-text elementor-post-info__item elementor-post-info__item--type-date']//time//text()").re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        # No more pages to scrap
        return None