from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from scraper.middlewares import HeadlessBrowserProxy
import scrapy
from typing import Optional

class MilkenInstitute(OCSpider):
    name = "MilkenInstitute"
    
    country = "US"

    start_urls_names = {
        "https://milkeninstitute.org/content-hub/news-releases?limit=100" : "News Releases"
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
        return "US/Eastern"
    
    def parse_intermediate(self, response):
        start_url =response.meta.get("start_url")
        page = response.meta.get('page', 0)
        page_url=f"{start_url}&page={page}"
        print(page_url)
        hbp = HeadlessBrowserProxy()
        yield scrapy.Request(
                hbp.get_proxy(page_url, timeout=30000), 
                callback=self.parse , 
                meta ={
                    "start_url": start_url,
                    "currentpage":page
                },
        )

    def get_articles(self, response) -> list:
        urls = response.xpath('//div[@class="title"]//a/@href').getall()
        article_urls=[]
        for url in urls:
            article_urls.append(response.urljoin(url).replace("https://proxy.scrapeops.io","https://milkeninstitute.org"))
        return article_urls

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="hero-article-copy"]//h1//text()').get()
        
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="node__content"]//p//text()').getall()) 
        
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%d %b %Y"
    
    def get_date(self, response) -> str:
        return response.xpath('//time/text()').get()
        
    def get_authors(self, response):
        return ""
    
    def get_page_flag(self) -> bool:
        return False
     
    def get_next_page(self, response,current_page ):
        page = response.meta.get('currentpage')
        current_page = page + 1
        has_articles = response.xpath('//div[@class="title"]//a')
        if has_articles:
            return current_page
        else: 
            return None
        
    def go_to_next_page(self, response, start_url, current_page: Optional[str] = "0"):
        next_page = self.get_next_page(response, current_page)
        start_url =response.meta.get("start_url")
        next_page_url=f"{start_url}&page={next_page}"
        request = scrapy.Request(
            url=next_page_url,
            callback=self.parse_intermediate  
        )
        request.meta.update({
            'start_url': response.meta.get('start_url'),
            'page': next_page
        })
        yield request        