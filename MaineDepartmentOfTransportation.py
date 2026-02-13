import scrapy
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class MaineDepartmentOfTransportation(OCSpider):
    name = 'MaineDepartmentOfTransportation'
    
    country = "US"

    start_urls_names = {
        'https://www.maine.gov/mdot/news/': 'CurrentYearNews',
        'https://www.maine.gov/mdot/news/archives/': 'Archives'
    }
    
    def parse_intermediate(self, response):
        articles = response.xpath('//div[@id = "years"]//div[@class= "accordion-container"]//a/@href').getall()
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
        articles = response.xpath('//div[@id = "years"]//div[@class= "accordion-container"]//a/@href').getall()
        unique_articles = list(set(articles)) 
        start_idx = response.meta.get('start_idx', 0)
        end_idx = start_idx + 100
        return unique_articles[start_idx:end_idx]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath("//h1/text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//*[@id="maincontent1"]/div[2]/p/text()').getall())
    
    def get_images(self, response, entry=None) :
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//*[@id="maincontent1"]/div[2]/p[2]/text()[1]').re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")

    def get_authors(self, response, entry=None) -> list[str]:
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        # No next page to scrape
        return None