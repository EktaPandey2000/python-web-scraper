from datetime import datetime
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from scraper.middlewares import HeadlessBrowserProxy
import scrapy

class OregonStateTreasury(OCSpider):
    name = "OregonStateTreasury"

    country="US"

    start_urls_names = {
        "https://www.oregon.gov/treasury/news-data/pages/news-releases.aspx":"News and Announcements",
    }

    charset = "utf-8"

    @property
    def source_type(self) -> str:
        return 'ministry'
    
    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Pacific"

    def parse_intermediate(self, response):
        hbp = HeadlessBrowserProxy()
        request = scrapy.Request(hbp.get_proxy(response.url, timeout=30000), callback=self.parse
        )
        request.meta['start_url'] = response.request.meta['start_url']
        yield request

    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="or-newsroom-article"]/a/@href').getall()
   
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('(//div[@class="col-md-8"])[2]/text()').get().strip()
       
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="col-md-8"]//p/text()').getall())
    
    def get_images(self, response, entry=None) :
        return response.xpath('//div[@class="col-md-12"]//img/@src').getall()
    
    def date_format(self) -> str:
        return "%Y-%m-%d"
    
    def get_date(self, response) -> str:
        date=response.xpath('//div[@class="col-md-8"]//span[2]//text()').getall()
        date_cleaned = ' '.join(date).strip()
        if date:
            date_obj = datetime.strptime(date_cleaned, "%B %d, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date

    def get_authors(self, response, entry=None) -> list[str]:
        return []
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No next page to scrape
        return None
