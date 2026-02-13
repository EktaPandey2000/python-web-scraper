from scraper.OCSpider import OCSpider
from typing import List, Union
import scrapy

class ArizonaStateTreasurersOffice(OCSpider):
    name = 'ArizonaStateTreasurersOffice'
 
    country = "US"

    start_urls_names = {
        'https://www.aztreasury.gov/press-releases/': 'NewsRoom',  
    }
    
    charset = 'iso-8859-1'

    article_data_map = {}  # Mapping date, pdf, title from start URL

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Eastern"

    def parse_intermediate(self, response):
        articles =set(response.xpath("//div[@data-mesh-id='comp-lm0pmo4vinlineContent']//p//a//@href").getall())
        total_articles = len(articles)
        articles_per_page = 100
        start_url = list(self.start_urls_names.keys())[0] 
        for start_idx in range(0,total_articles, articles_per_page):    # Indexing for virtual pagination to extract more than 100 articles from single page
            yield scrapy.Request(
                url=start_url,  
                callback=self.parse,
                meta={'start_idx': start_idx, 'start_url': start_url},  
                dont_filter=True
            )

    def get_articles(self, response) -> list:  
        try:
            articles_with_duplicate = response.xpath("//div[@data-mesh-id='comp-lm0pmo4vinlineContent']//p")
            all_articles = set()  
            for article in articles_with_duplicate:
                full_url = article.xpath(".//a/@href").get()
                title = article.xpath(".//a/text()").get() 
                date = article.xpath("./text()").get()
                if full_url: 
                    if not title:
                        title = response.xpath("//title/text()").get(default="").strip()
                    if not date:
                       date = response.xpath("//meta[@name='date']/@content").get(default="").strip()
                    self.article_data_map[full_url] = {  # Mapping done for indexing articles and PDF's from start URL
                            "title": title.strip(),
                            "date": date.strip().replace("\xa0", " "),
                            "pdf": [full_url]
                        }
                    all_articles.add(full_url)
            all_articles = list(all_articles)
            start_idx = response.meta.get('start_idx', 0) # Indexing should be called from parse_intermediate only
            end_idx = start_idx + 100 
            return all_articles[start_idx:end_idx] # Article url's are extracted and returned
        except Exception as e:
            return []
            
    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("title", "")

    def get_body(self, response) -> str:
        # Only PDF's are there to scrap
        return ""

    def get_images(self, response) -> List[str]:
        # Only PDF's are there to scrap
        return []

    def date_format(self) -> str:
        return "%m-%d-%Y"

    def get_date(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("date", "")

    def get_authors(self, response):
        # Only PDF's are there to scrap
        return []
    
    def get_document_urls(self, response, entry=None):
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("pdf", [])
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> Union[None, List[str]]:
        # No next page to scrap
        return None