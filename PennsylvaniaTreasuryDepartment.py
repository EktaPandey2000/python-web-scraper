from datetime import datetime
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class PennsylvaniaTreasuryDepartment(OCSpider):
    name = "PennsylvaniaTreasuryDepartment"

    country="US"

    start_urls_names = {
        "https://www.patreasury.gov/newsroom/":"News and Announcements",
    }

    charset = "utf-8"
    
    @property
    def language(self):
        return "English"

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "US/Eastern"
    
    def get_articles(self, response) -> list:
        return response.xpath('//h2[@class="entry-title"]//a/@href').getall()
   
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//h2[@class="entry-title"]//text()').get().strip()   
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="col-md-12 col-sm-12"]//p/text()').getall())
    
    def get_images(self, response, entry=None) :
        return response.xpath('//div[@class="col-md-12"]//img/@src').getall()

    def date_format(self) -> str:
        return "%Y-%m-%d"
    
    def get_date(self, response) -> str:
        date=response.xpath('//div[@class="posted-date pull-left"]/span//text()').getall()
        date_cleaned = ' '.join(date).strip()
        if date:
            date_obj = datetime.strptime(date_cleaned, "%d %B, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            return formatted_date

    def get_authors(self, response, entry=None) -> list[str]:
        return []
    
    def get_document_urls(self, response, entry=None):
        return response.xpath('//div[@class="col-md-12 col-sm-12"]//p/a/@href').getall()
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        return response.xpath('//li[.= "Next"]//a/@href').get()   # . ->Refers to the current node (the <li> element in this case)