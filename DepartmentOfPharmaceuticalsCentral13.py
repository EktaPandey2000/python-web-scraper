import re
from urllib.parse import unquote
from scraper.OCSpider import OCSpider
#13(T1)
class DepartmentOfPharmaceuticalsCentral13(OCSpider):
    name = 'DepartmentOfPharmaceuticalsCentral13'
    source = 'DepartmentOfPharmaceuticalsCentral'
    language = "English"
    country = 'India'
    charset = "iso-8859-1"

    HEADLESS_BROWSER_WAIT_TIME = 5000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350,
        },
        "DOWNLOAD_DELAY": 3,
    }

    start_urls_names = {
        'https://pharma-dept.gov.in/detailed-demand-grants':""
    }

    start_url_with_no_pagination = {
        "https://pharma-dept.gov.in/detailed-demand-grants"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_map = {}
    def get_articles(self, response) -> list:
        article_link = response.xpath("//tbody//tr//td[3]/a/@href").getall()
        title_link = response.xpath("//tbody//tr//td[2]/text()").getall()
        if len(title_link) != len(article_link):
            print( "response.url is not Matching the title to the article_links ",response.url,)
            return []
        for i in range(len(article_link)):
            self.url_to_title_map[article_link[i].rsplit("/", 1)[1]] = [title_link[i] , article_link[i]]
        return article_link

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            title = self.url_to_title_map[url][0]
            return title.strip()
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y-%y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            date = self.url_to_title_map[url][0]
        match = re.search(r"(20\d{2})-(\d{2})", date)
        if match:
            return match.group(0)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [unquote(response.url)]

    def get_next_page(self, response) -> str:
        return None