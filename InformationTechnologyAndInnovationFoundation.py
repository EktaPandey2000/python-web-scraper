from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime
from typing import Optional

class InformationTechnologyAndInnovationFoundation(OCSpider):
    name = 'InformationTechnologyAndInnovationFoundation'
    
    country = "US"

    proxy_country = "us"

    HEADLESS_BROWSER_WAIT_TIME = 10000  # 10 seconds wait time

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.HeadlessBrowserProxy': 350,
            },
        "DOWNLOAD_DELAY": 1
    }

    start_urls_names = {
        'https://itif.org/publications/press-releases/': 'Press Release',
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
        urls = response.xpath('//a[@class="block mb-3 hover:underline"]/@href').getall()
        article_urls=[]
        for url in urls:
            article_urls.append(response.urljoin(url))
        return article_urls
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[@class="page-heading text-35  font-gothicprobold"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//blockquote/em/text() | //p//text()').getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        raw_date = response.xpath('normalize-space(//div[@class="block lg:inline-block"]/text())').get()
        try:
            date_obj = datetime.strptime(raw_date, "%B %d, %Y")
            return date_obj.strftime(self.date_format())
        except Exception:
            return ""

    def get_authors(self, response):
        return []

    def get_page_flag(self) -> bool:
        return False
  
    def get_next_page(self, response) -> Optional[str]:
        current_url = response.url
        if 'page=' in current_url:
            current_page = int(current_url.split('page=')[-1])
        else:
            current_page = 1
        next_button_exists = response.xpath('//li[@class="next"]/a')
        if not next_button_exists:
            return None
        next_page = current_page + 1
        next_page_url = f"https://itif.org/publications/press-releases/?page={next_page}"
        return next_page_url