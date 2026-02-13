import re
from urllib.parse import urljoin
from scraper.OCSpider import OCSpider
#3(T1)
class DepartmentOfPharmaceuticalsCentral3(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral3"
    source = "DepartmentOfPharmaceuticalsCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.pharma-dept.gov.in/annual-report":''
    }

    start_url_with_no_pagination = {
        "https://www.pharma-dept.gov.in/annual-report"
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
        article_links = response.xpath("//tbody//tr//td[3]//a/@href").getall()
        title_links = response.xpath("//tbody//tr//td[2]/text()").getall()
        if len(title_links) != len(article_links):
            print("response.url is not Matching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return urljoin("https://www.pharma-dept.gov.in", entry.strip())

    def get_title(self, response) -> str:
        filename = response.url.rsplit("/", 1)[-1]
        if filename in self.url_to_title_map:
            title = self.url_to_title_map[filename][0]
            title = title.strip()
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y-%y"

    def get_date(self, response, title_links=None) -> str:
        if title_links:
            return response.xpath(title_links).re_first(r"\b\d{4}-\d{2}\b")
        title = self.get_title(response)
        if title:
            match = re.search(r"\b\d{4}-\d{2}\b", title)
            if match:
                return match.group(0)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response):
        return None