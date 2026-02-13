from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class ForeignPolicyResearchInstitute(OCSpider):
    name = 'ForeignPolicyResearchInstitute'
    
    country = "US"

    proxy_country = "us"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.GeoProxyMiddleware': 350
            }
    }

    start_urls_names = {
        'https://www.fpri.org/articles/': 'Articles'
    }
    
    charset = "utf-8"
    
    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Eastern"
    
    def get_articles(self, response) -> list:
        return response.xpath("//h5/a/@href").getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h2[@class="caption-article"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//li/span/text()').re_first(r"[A-Za-z]+ \d{1,2}, \d{4}")
    
    def get_authors(self, response):
        return response.xpath('//div[@class="author-url-left"]//a[@class="author"]/text()').get()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath('//a[@class="next page-numbers"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None