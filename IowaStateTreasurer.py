from urllib.parse import urlparse, urlunparse
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import date

class IowaStateTreasurer(OCSpider):
    name = 'IowaStateTreasurer'
    
    country = "US"

    todays_date = date.today()
    
    year = todays_date.year

    start_urls_names = {
        f'https://www.iowatreasurer.gov/news/isave-529/archive/{year}':'ISave 529',
        f'https://www.iowatreasurer.gov/news/general-treasury/archive/{year}':'General Treasury',
        f'https://www.iowatreasurer.gov/news/great-iowa-treasure-hunt/archive/{year}':'Great Iowa Treasure Hunt',
        f'https://www.iowatreasurer.gov/news/iable/archive/{year}':'IAble'
    }
    
    charset = "utf-8"
    
    @property   
    def language(self):
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "US/Central"
    
    def get_articles(self, response) -> list:
        return response.xpath("//div[@id = 'news_module']//article//h2//a/@href").getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return response.xpath("//div[@class='inside-page-header-content-wrap']//h1//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='cms_content']//p//text()").getall())
    
    def get_images(self, response) -> list[str]:
        return response.xpath("//div[@class='cms_content']//img//@src").getall()
    
    def date_format(self) -> str:
        return "%B %d, %Y"
    
    def get_date(self, response) -> str:
        return response.xpath("//div[@class='cms_metadata2 cms_date']//h3//text()").re_first(r"([A-Za-z]+ \d{1,2}, \d{4})")
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> str:
        try:
            next_page = response.xpath("//div[@class='pagination-next-page pagination-bg']//a/@href").get()
            if next_page:
                return response.urljoin(next_page)
            else:
                parsed_url = urlparse(response.url)
                url_parts = parsed_url.path.split("/")
                if url_parts[-1].isdigit():
                    current_year = int(url_parts[-1])
                    if response.status == 200: 
                        previous_year = current_year - 1
                        url_parts[-1] = str(previous_year)
                        new_url = urlunparse(parsed_url._replace(path="/".join(url_parts)))
                        return new_url
        except Exception as e:
            self.logger.error(f"Error extracting next page link from page {response.url}: {e}")
            return None