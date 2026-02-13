from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime

class TexasDepartmentOfTransportation(OCSpider):
    name = "TexasDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://www.txdot.gov/about/newsroom/statewide.html": "News releases",
    }

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350
            },
        "DOWNLOAD_DELAY": 2,
        "DUPEFILTER_CLASS": 'scrapy.dupefilters.BaseDupeFilter',
    }

    HEADLESS_BROWSER_WAIT_TIME = 20000

    charset = "utf-8"
    
    visited_links = set()
    
    year = datetime.now().year
    
    @property
    def language(self):
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def timezone(self):
        return "America/Denver"
    
    def get_articles(self, response) -> list:
        base_url = "https://www.txdot.gov"
        article_year = (self.year - 1)
        if response.url == self.start_urls[0]:  # If it's the start URL
            links = response.xpath('//a[@class="cmp-list__item-link"]/@href').getall()
            # Filter out links that contain a past year
            links = [
                link for link in links
                if not any(str(year) in link for year in range(2012, article_year + 1))
            ]
        else:  # If it's a next page
            links = response.xpath('//table[@class="table-el table-el-bordered table-sort table-filter"]//tbody//tr//td/a/@href').getall()  # Get links from articles table
        links = [base_url + link if link.startswith("/") else link for link in links]
        return links
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//div[@class="pb-2 text-left "]/h1/text()').get()
    
    def get_body(self, response) -> str:
        body =  body_normalization(response.xpath('//div[@class=" mb-5"]//text()').getall()) or body_normalization(response.xpath('//div[@class= " mb-0"]//p/text()').getall())
        if body:
            return body
        else:
            return body_normalization(response.xpath('//div[@class= "news-release-content"]//p/text()').getall())
    
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return "%m/%d/%Y"
    
    def get_date(self, response) -> Optional[str]:
        raw_date = (
            response.xpath('//small[@class="contact-card-text" and @data-date-longmonthtoshort]/text()').get() or
            response.xpath('//div[contains(@class, "mb-0")]/p[1]/text()').get()
        )
        if not raw_date:
           return None
        raw_date = raw_date.strip()
        for date_format in ["%B %d, %Y", "%b. %d, %Y"]:
                    try:
                        parsed_date = datetime.strptime(raw_date, date_format)
                        return parsed_date.strftime("%m/%d/%Y")
                    except ValueError:
                        continue
        return None
    
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) -> Optional[str]:
        base_url = "https://www.txdot.gov/about/newsroom/statewide"
        current_year = datetime.now().year
        # Start checking from last year
        for year in range(current_year - 1, 2012, -1):  # Iterate backward until 2012
            next_page_url = f"{base_url}/{year}.html"
            # Ensure it's not already visited
            if next_page_url not in self.visited_links:
                self.visited_links.add(next_page_url)
                return next_page_url