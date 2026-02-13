import re
from scraper.OCSpider import OCSpider
# 11(T1)
class DepartmentOfPharmaceuticalsCentral11(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral11"
    source= "DepartmentOfPharmaceuticalsCentral"
    country= "India"
    language= "English"
    charset = "iso-8859-1"
    exclude_rules = ["https://smdi.lsssdc.in"]

    start_urls_names = {
        "https://pharma-dept.gov.in/budget-and-expenditure":"",
        "https://pharma-dept.gov.in/schemes/scheme-strengthening-medical-device-industry": "",
        "https://www.pharma-dept.gov.in/proactive-disclosure": ""
    }

    start_urls_with_no_pagination_set = {
        "https://pharma-dept.gov.in/schemes/scheme-strengthening-medical-device-industry"
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
        article_links = response.xpath("//a[contains(@href, '.pdf') and not(ancestor::footer)]").getall()
        title_links = response.xpath("//td[@class='views-field views-field-php']//ul//li//a/text()").getall()
        if len(title_links) != len(article_links):
            print("response.url is not Matching the date and title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [article_links[i] , title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_title_map:
            title= self.url_to_title_map[url][1]
            title=title.strip()
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%d-%m-%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            date = self.url_to_title_map[url][0]
            match = re.search(r"(\d{1,2})\.(\d{1,2})\.(\d{4})", date)
            if match:
                date = match.group(0)
                date= date.replace(".", "-")
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None