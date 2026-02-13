from datetime import datetime
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class NorthDakotaStateTreasurer(OCSpider):
    name = "NorthDakotaStateTreasurer"

    country="US"

    start_urls_names = {
        "https://www.treasurer.nd.gov/news":"News",
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
        return "US/Central"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="media-heading"]//a/@href').getall()
   
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//span[@class="field field--name-title field--type-string field--label-hidden"]//text()').get()
       
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"]//p//text()').getall())
    
    def get_images(self, response, entry=None) :
        return []
    
    def date_format(self) -> str:
        return "%A,%Y-%m-%d"
    
    def get_date(self, response) -> str:
        date = response.xpath('//span[@class="news-date"]//text()').get().strip()
        # Two date formats listed in the child articles
        if date:
            try :
                date_obj = datetime.strptime(date, "%A, %B %d, %Y")
                formatted_date = date_obj.strftime("%A,%Y-%m-%d")
                return formatted_date
            except ValueError:
                pass
            try :
                date_obj =datetime.strptime(date, "%A, %B %d, %Y - %I:%M%p")
                formatted_date=date_obj.strftime("%A,%Y-%m-%d")
                return formatted_date
            except ValueError:
                pass

    def get_authors(self, response, entry=None) -> list[str]:
        return []
    
    def get_document_urls(self, response, entry=None):
        return response.xpath('//div[@class="clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item"]//p//a/@href').getall()
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No next pages to scrape
        return None