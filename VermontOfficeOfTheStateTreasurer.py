from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class VermontOfficeOfTheStateTreasurer(OCSpider):
    name = "VermontOfficeOfTheStateTreasurer"

    country="US"

    start_urls_names = {
        "https://www.vermonttreasurer.gov/content/press-releases": "",
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
        return "America/New_York"
    
    def get_articles(self, response) -> list:
        return response.xpath('//div[@class="views-row"]/article/h2/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="usa-layout-docs__main padding-bottom-2 tablet:padding-bottom-0 desktop:grid-col-9"]//h1[@class="margin-0"]/span[@property="dc:title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="usa-prose field field--name-body field--type-text-with-summary field--label-hidden field__item"]//p//text()').getall())

    def get_images(self, response) -> list:
        return response.xpath('//div[@class="field field--name-field-widget-image-2 field--type-image field--label-hidden field__item"]//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> Optional[str]:
        date_str = (response.xpath('//div[@class="field field--name-field-date field--type-datetime field--label-hidden field__item"]/text()').get() or "").strip()
        return datetime.strptime(date_str, "%B %d, %Y").strftime("%m-%d-%Y") 

    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        next_page = response.xpath('//ul[@class="usa-pagination__list js-pager__items"]//a[contains(@class, "usa-pagination__next-page")]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None