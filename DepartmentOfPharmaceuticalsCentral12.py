import re
from datetime import date
from urllib.parse import urljoin
from scraper.OCSpider import OCSpider
#12(T2)
class DepartmentOfPharmaceuticalsCentral12(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral12"
    source = "DepartmentOfPharmaceuticalsCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://pharma-dept.gov.in/budget-and-expenditure": ""
    }

    start_url_with_no_pagination = {
        "https://pharma-dept.gov.in/budget-and-expenditure"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_and_date_map = {}
    def get_articles(self, response) -> list:
        datetime_strs = response.xpath("//div[@class='field-content']//h2//text()").getall()
        article_links = response.xpath("//div[@class='embed_title_download']//a/@href").getall()
        title_links = response.xpath("//div[@class='field-content']//h1//text()").getall()
        if len(title_links) != len(article_links) or len(datetime_strs) != len(article_links):
            print("response.url is not Matching the date and title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_and_date_map[article_links[i].rsplit("/", 1)[1]] = [datetime_strs[i], title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return urljoin("https://www.pharma-dept.gov.in", entry.strip())

    def get_title(self, response) -> str:
        filename = response.url.rsplit("/", 1)[-1]
        if filename in self.url_to_title_and_date_map:
            return self.url_to_title_and_date_map[filename][0]
        return None

    def date_format(self) -> str:
        return "%d-%m-%Y"

    def get_date(self, response, date=None) -> str:
        url = response.url.rsplit("/", 1)[-1]
        if url in self.url_to_title_and_date_map:
            date_text = self.url_to_title_and_date_map[url][0]
            match = re.search(r"\b\d{1,2}[./-]\d{1,2}[./-]\d{4}\b", date_text)
            if match:
                # Convert separators to '-'
                return re.sub(r"[./]", "-", match.group(0))
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if entry and any(ext in entry.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [self.get_href(entry)]
        return []

    def get_next_page(self, response):
        return None