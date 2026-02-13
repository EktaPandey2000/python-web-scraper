from scraper.OCSpider import OCSpider
from typing import List
from scraper.utils.helper import body_normalization

class NewJerseyAttorneyGeneral(OCSpider):
    name = 'NewJerseyAttorneyGeneral'
    
    country = "US"
    
    start_urls_names = {
        'https://www.njoag.gov/programs/nj-cares/press-releases/': "Press Releases"
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
        return response.xpath("//div[@class='et_pb_ajax_pagination_container']//h2//a/@href").getall()

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath("//div[@class='et_post_meta_wrapper']//h1/text()").get()
    
    def get_body(self, response) -> str:
        body = body_normalization(response.xpath("//div[@class='et_pb_row et_pb_row_2']//p//text() | //div[@class='et_pb_row et_pb_row_2']//ul//li//text()").getall()) #for page 1,2,4
        if not body:
            body = body_normalization(response.xpath("//div[@class='et_pb_row et_pb_row_1']//p//text() | //div[@class='et_pb_row et_pb_row_1']//ul//li//text()").getall()) #for page 3
        return body
    
    def get_images(self, response) -> list:
        return response.xpath("//div[@class='et_pb_row et_pb_row_2']//img//@src").getall()
    
    def date_format(self) -> str:
        return "%b %d, %Y"

    def get_date(self, response) -> str:
        return response.xpath("//div[@class='et_post_meta_wrapper']//p/span[@class='published']/text()").get()
    
    def get_authors(self, response): 
        return []
            
    def get_document_urls(self, response, entry=None) -> List[str]:    
        pdf = response.xpath("//div[@class='et_pb_module et_pb_text et_pb_text_3  et_pb_text_align_left et_pb_bg_layout_light']//a[contains(@href,'.pdf')]//@href").get()#xpath for 1, 2 pages
        if not pdf:
            pdf = response.xpath("//div[@class='et_pb_module et_pb_text et_pb_text_2  et_pb_text_align_left et_pb_bg_layout_light']//a[contains(@href,'.pdf')]//@href").get()#xpath for 3, 4 pages
        return pdf
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        next_page = response.xpath("//div[@class='alignleft']//a[contains(text(), 'Older Entries')]//@href").get()
        if next_page:
            return next_page
        else:
            return None