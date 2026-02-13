from typing import List, Union
from scraper.OCSpider import OCSpider
import scrapy

class IllinoisStateTreasurersOffice(OCSpider):
    name = "IllinoisStateTreasurersOffice"
    
    country = "US"
    
    start_urls_names = {
        "https://illinoistreasurer.gov/Office_of_the_Treasurer/Media_Center/Press_Releases": "Press Releases",
    }
    
    article_data_map = {}  # Mapping date, pdf, title from start URL
    
    def parse_intermediate(self, response):
            articles = response.xpath("//div[@class='accrodation']//div[@class='content']/a/@href").getall()
            total_articles = len(articles)
            start_url = list(self.start_urls_names.keys())[0] 
            for start_idx in range(0,total_articles, 100):  # Indexing for virtual pagination to extract more than 100 articles from single page
                yield scrapy.Request(
                url=start_url,  
                callback=self.parse,
                meta={'start_idx': start_idx, 'start_url': start_url},  
                dont_filter=True
            )
                
    charset = 'iso-8859-1'
     
    @property
    def language(self):
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self) -> str:
        return "America/Chicago"
                
    def get_articles(self, response) -> list:
        try:
            articles_with_duplicate = response.xpath("//div[@class='accrodation']//div[@class='content']/a/@href").getall()
            title_dates = response.xpath("//div[@class='accrodation']//a[@href='#']/text()").getall()
            all_articles = set()
            for i in range(len(articles_with_duplicate)):
                full_url = articles_with_duplicate[i]
                title = ""
                date = ""
                if i < len(title_dates):
                    title_date = title_dates[i].split(" - ", 1)
                    if len(title_date) > 1:
                        title = title_date[1]
                        date = title_date[0]
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
            return all_articles[start_idx:end_idx]  # Article url's are extracted and returned
        except Exception as e:
            return []

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("title", "")

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> List[str]:
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("date", "").strip()
    
    def get_authors(self, response) -> List[str]:
        return []

    def get_document_urls(self, response, entry=None) -> List[str]:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("pdf", [])

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> Union[None, str]:
        return None