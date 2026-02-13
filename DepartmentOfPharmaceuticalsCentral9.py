import re
from scraper.OCSpider import OCSpider
#9(T1)
class DepartmentOfPharmaceuticalsCentral9(OCSpider):
    name = 'DepartmentOfPharmaceuticalsCentral9'
    source = 'DepartmentOfPharmaceuticalsCentral'
    language = "English"
    country = 'India'
    charset = "iso-8859-1"

    start_urls_names = {
        'https://www.pharma-dept.gov.in/cpses': ''
    }

    start_urls_with_no_pagination_set = {
        "https://www.pharma-dept.gov.in/cpses"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_article_map = {}
    def get_articles(self, response) -> list:
        article_link = response.xpath("//div[@class='embed_title_download']/a/@href").getall()
        title_link = response.xpath("//div[@class='inner-right-content ']//h1[@class='heading']//text()").getall()
        for i in range(len(article_link)):
            self.url_to_article_map[article_link[i].rsplit("/", 1)[1]] = [title_link[i] , article_link[i]]
        return article_link

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_article_map:
            title = self.url_to_article_map[url][0]
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
        if url in self.url_to_article_map:
            date = self.url_to_article_map[url][1]
        match = re.search(r"(20\d{2})-(\d{2})", date)
        if match:
            return match.group(0)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None