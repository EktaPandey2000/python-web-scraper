from scraper.OCSpider import OCSpider
import scrapy
from scraper.middlewares import HeadlessBrowserProxy

class BusinessOregon(OCSpider):
    name = "BusinessOregon"

    country="US"

    start_urls_names = {
        "https://www.oregon.gov/biz/newsroom/Pages/default.aspx?wp6256=l:100#g_43757c9a_540a_4885_be9a_f8499b6fa5fd" :"Press Releases"
    }
    
    def parse_intermediate(self, response):
        hbp = HeadlessBrowserProxy()
        request = scrapy.Request(hbp.get_proxy(response.url, timeout=30000), callback=self.parse
        )
        request.meta['start_url'] = response.request.meta['start_url']
        yield request

    charset="iso-8859-1"

    @property
    def language(self) :
        return "English"

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "US/Eastern"
    
    article_data_map = {}  # Mapping date with articles from start URL
    
    def get_articles(self, response) -> list:
        self.extract_articles_with_dates(response)
        urls = response.xpath('//tr[@role="row"]//a/@href').getall()
        article_urls=[]
        for url in urls:
            article_urls.append(response.urljoin(url).replace("https://proxy.scrapeops.io","https://www.oregon.gov"))
        return article_urls
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return self.article_data_map[response.request.meta.get('entry')].get("title")
        
    def get_body(self, response) -> str:
        # Only PDF's are there to scrape
        return ""

    def get_images(self, response) -> list[str]:
        # Only PDF's are there to scrape
        return []

    def date_format(self) -> str:
        return "%m/%d/%Y"
    
    def get_date(self, response) -> str:
        return self.article_data_map[response.request.meta.get('entry')].get("date")

    def get_authors(self, response):
        # Only PDF's are there to scrape
        return ""
    
    def get_document_urls(self, response, entry=None):
        return self.article_data_map[response.request.meta.get('entry')].get("pdf")
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No next page to scarpe
        return None
    
    def extract_articles_with_dates(self, response):
        mapping = {}
        for article in response.xpath('//tr[@role="row"]'):
            url = article.xpath(".//a/@href").get()
            title = article.xpath(".//a/text()").get()
            date = article.xpath(".//td/text()").get()
            if url and title and date:
                full_url = response.urljoin(url.strip()).replace("https://proxy.scrapeops.io","https://www.oregon.gov")
                clean_date=date.strip()
                mapping[full_url] = {"title": title.strip(), "date": clean_date, "pdf": [full_url]}
            self.article_data_map.update(mapping)
        print(mapping)
        return self.article_data_map