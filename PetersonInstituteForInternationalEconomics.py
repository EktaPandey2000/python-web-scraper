from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class PetersonInstituteForInternationalEconomics(OCSpider):
    name = 'PetersonInstituteForInternationalEconomics'
    
    country = "US"

    proxy_country = "us"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.GeoProxyMiddleware': 350
            },
        "DOWNLOAD_DELAY": 1
    }

    start_urls_names = {
        'https://www.piie.com/newsroom': 'Press Release'
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
    
    def get_articles(self, response) :
        return [response.urljoin(url) for url in response.xpath('//h2[@class="teaser__title"]//a/@href').getall()]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="hero-banner-publication__title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:    
        return response.xpath('//div[@class="hero-banner-publication__date"]/time/text()').re_first(r"[A-Za-z]+ \d{1,2}, \d{4}")

    def get_authors(self, response):
        return ""

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath('//li[contains(@class, "pager__item--next")]/a/@href').get()
        if next_page:
            return response.urljoin(next_page)
        return None