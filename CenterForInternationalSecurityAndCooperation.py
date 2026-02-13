from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class CenterForInternationalSecurityAndCooperation(OCSpider):
    name = 'CenterForInternationalSecurityAndCooperation'
    
    country = "US"

    custom_settings = {
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter'
    }

    start_urls_names = {
        'https://cisac.fsi.stanford.edu/news': 'News'
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
        articles = response.xpath('//a[@class="h__link"]/@href').getall()
        return [response.urljoin(link) for link in articles]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//div[@class="node news title string label-hidden"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        date = response.xpath('normalize-space(//li[@class="breadcrumb__item"]/time/text())').get()
        if date:
            try:
                dt = datetime.strptime(date, self.date_format())
                return dt.strftime(self.date_format())
            except ValueError:
                return ""
        else:    
            return ""

    def get_authors(self, response):
        return response.xpath('//li[contains(@class, "authors-list__item")]//a[contains(@class, "authors-list__link")]/text()').getall()

    def get_document_urls(self, response, entry = None) -> list[str]:
        return []

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath('//li[contains(@class, "pager__item--next")]//a[@class="pager__link pager__link--next"]/@href').get()
        if next_page:
            next_page_url = response.urljoin(next_page)
            return next_page_url