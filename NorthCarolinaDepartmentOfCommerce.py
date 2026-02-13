from scraper.utils.helper import body_normalization
from scraper.OCSpider import OCSpider

class NorthCarolinaDepartmentOfCommerce(OCSpider):
    name = 'NorthCarolinaDepartmentOfCommerce'

    country = "US"

    start_urls_names = {
        "https://www.commerce.nc.gov/news/press-releases": "News",
    }

    charset = "utf-8"
    
    @property
    def source_type(self) -> str:
        return 'ministry'
    
    @property
    def timezone(self):
        return "US/Eastern"
    
    @property
    def language(self):
        return "English"
    
    def get_articles(self, response) -> list:
        return response.xpath("//h2//a//@href").getall()
        
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath("//h1//span//text()").get()
        
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='row gx-5']//div[@class='clearfix text-formatted field field--name-body field--type-text-with-summary field--label-hidden field__item']//p//text()").getall())
    
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%A, %B %d, %Y"
    
    def get_date(self, response) -> str:
        date = response.xpath("//div[@class='press_release__title col-12 col-lg-12 noimage']//date//text()").get()
        if not date:
            date = response.xpath("//div[@class='press_release__title col-12 col-lg-7']//date//text()").get()
        return date
    
    def get_authors(self, response):
        return response.xpath("//div[@class='field field--name-field-city-location field--type-string field--label-hidden field__item']//text()").get()
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response) -> str:
        next_page=response.xpath("//ul[@class='pagination js-pager__items']//li//a[contains(@title,'next page')]//@href").get()
        if next_page:
            return next_page
        else:
            return None