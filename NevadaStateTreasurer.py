from scraper.OCSpider import OCSpider
import re
from typing import List

class NevadaStateTreasurer(OCSpider):
    name = 'NevadaStateTreasurer'
    
    country = "US"

    start_urls_names = {
        'https://www.nevadatreasurer.gov/PublicInfo/Public_Notices/': 'Public Notices'
    }
    
    article_data_map = {}
    
    charset = "iso-8859-1"
    
    @property
    def language(self):
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "US/Pacific"
    
    def get_articles(self, response) -> list:
        try:
            articles = response.xpath("//div[@class='col-md-8']//table//tr")
            article_urls = []
            for article in articles:
                url = article.xpath(".//a/@href").get()
                title = article.xpath(".//a/text()").get()
                date_text = article.xpath(".//td/text()").get()
                if url and title and date_text:
                    full_url = response.urljoin(url.strip())
                    date_text = date_text.strip()
                    date_text = re.sub(r'\(pdf\)', '', date_text).strip()  # Remove "(pdf)" 
                    date_text = date_text.replace("\xa0", " ")
                    self.article_data_map[full_url] = {
                        "title": title.strip(),
                        "date": date_text,
                        "pdf": [full_url]
                    }
                    article_urls.append(full_url)
            return article_urls
        except Exception as e:
            self.logger.error(f"Error fetching articles: {e}")
            return []

    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self,response) -> str:
        return self.article_data_map[response.request.meta.get('entry')].get("title")
    
    def get_body(self, response) -> str:
        # Only PDF's are there to scrap
        return ""
    
    def get_images(self, response, entry=None) -> List[str]:
        # Only PDF's are there to scrap
        return []
    
    def date_format(self) -> str:
        return "%m/%d/%Y" 

    def get_date(self, response) -> str:
        return self.article_data_map[response.request.meta.get('entry')].get("date")
    
    def get_authors(self, response):
        # Only PDF's are there to scrap
        return []

    def get_document_urls(self, response, entry=None):
        return self.article_data_map[response.request.meta.get('entry')].get("pdf")
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response, current_page):
        # No next page to scrap
        return None