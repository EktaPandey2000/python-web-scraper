from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class MiddleEastInstitute(OCSpider):
    name = 'MiddleEastInstitute'
    
    country = "US"

    start_urls_names = {
        'https://www.mei.edu/search?search=&field_term_region=All&type=5&field_term_center=All': 'Blogs'
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
        return [response.urljoin(url) for url in response.xpath('//article[@class="feature feature-1"]//h4/a/@href').getall()]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath('//h1[starts-with(@class, "node-id")]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return []
    
    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        return response.xpath('//date[@class="post__date"]/text()').re_first(r"[A-Za-z]+ \d{1,2}, \d{4}")

    def get_authors(self, response):
        return response.xpath('//p[@class="post__author"]//a/text()').getall()

    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        next_page = response.xpath('//a[@rel="next"]/@href').get()
        if next_page:
            return response.urljoin(next_page)
        else:
            return None