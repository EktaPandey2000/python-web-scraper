from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 

class UtahStateTreasurerOffice(OCSpider):
    name = "UtahStateTreasurerOffice"

    country="US"

    start_urls_names = {
        "https://treasurer.utah.gov/news-room/": "News Room",
    }

    charset = "utf-8"

    article_date_map = {}  # Mapping dates with articles from start URL to extract date from start URL as dates are not present in child articles

    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def language(self): 
        return "English"
    
    @property
    def timezone(self):
        return "America/Denver"
    
    def get_articles(self, response) -> list:
        self.extract_articles_with_dates(response)
        return [response.urljoin(link) for link in response.xpath("//div[@class='x-recent-posts cf vertical']/a/@href").getall()]
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="entry-wrap"]//h1/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="entry-content content"]//p//text()').getall())

    def get_images(self, response) -> list:
        return response.xpath('//div[@class="entry-content content"]//img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> str:
        date_str = self.article_date_map.get(response.url)
        date_obj = datetime.strptime(date_str, "%B %d, %Y")  
        return date_obj.strftime("%m-%d-%Y") 
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]: 
        # No next page to scrap
        return None
    
    def extract_articles_with_dates(self, response):
        # Function to extract articles date from start URL
        for article in response.xpath("//div[@class='x-recent-posts cf vertical']/a"):
            url = article.xpath("./@href").get()
            date = article.xpath(".//span[@class='x-recent-posts-date']/text()").get()
            self.article_date_map[response.urljoin(url)] = date.strip()
        return self.article_date_map