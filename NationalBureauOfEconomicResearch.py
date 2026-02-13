from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class NationalBureauOfEconomicResearch(OCSpider):
    name = 'NationalBureauOfEconomicResearch'
    
    country = "US"

    HEADLESS_BROWSER_WAIT_TIME = 10000  # 10 seconds wait time

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.HeadlessBrowserProxy': 350
            },
        "DOWNLOAD_DELAY": 1
    }

    start_urls_names = {
        'https://www.nber.org/nber-news?page=1&perPage=50': 'Press Release'
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
        urls = response.xpath('//div[@class="digest-card__title"]/a/@href').getall()
        article_urls=[]
        for url in urls:
            article_urls.append(response.urljoin(url))
        return article_urls
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="page-header__title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date_str = response.xpath('//div[@class="page-header__citation-info"]/time/@datetime').get()
        if date_str:
            try:
                date_obj = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%SZ")
                return date_obj.strftime(self.date_format())
            except Exception:
                return ""
        else:    
            return ""

    def get_authors(self, response):
        return ""

    def get_page_flag(self) -> bool:
        return False
  
    def get_next_page(self, response) -> Optional[str]:
        if not response.xpath('//div[@class="digest-card__title"]/a'):
            return None
        url = response.url
        current_page = 1
        if "page=" in url:
            try:
                current_page = int(url.split("page=")[1].split("&")[0])
            except ValueError:
                current_page = 1
        next_page = current_page + 1
        next_url = f"https://www.nber.org/nber-news?page={next_page}&perPage=50"
        return next_url