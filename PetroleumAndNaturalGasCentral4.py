from scraper.OCSpider import OCSpider
from urllib.parse import unquote
#4(T2)
class PetroleumAndNaturalGasCentral4(OCSpider):
    name = "PetroleumAndNaturalGasCentral4"
    source = "PetroleumAndNaturalGasCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = ["https://mopng.gov.in/files/natural-gas/policies-and-guidelines/consolidated gas allocation policies.pdf",
                     "https://mopng.gov.in/files/natural-gas/policies-and-guidelines/PMP ACT 1962.pdf"]

    start_urls_names = {
        "https://mopng.gov.in/en/natural-gas/policies-guidelines":""
    }

    start_urls_with_no_pagination_set = {
        "https://mopng.gov.in/en/natural-gas/policies-guidelines"
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
        articles = []
        for i in response.xpath("//tbody//tr"):
            url = i.xpath(".//td[3]//a/@href").get()
            title = i.xpath(".//td[@class='views-field views-field-title'][2]/text()").get()
            date = i.xpath(".//td[@class='views-field views-field-field-start-date'][1]//span//text()").get()
            if not (url and title and date):
                continue
            if url and title and date:
                full_url = unquote(url.rsplit("/", 1)[1])
                self.url_to_title_and_date_map[full_url] = [title, date]
                articles.append(url)
        return articles

    def get_href(self, entry) -> str:
        return f"https://mopng.gov.in{entry}"

    def get_title(self, response) -> str:
        url=  unquote(response.url.rsplit("/", 1)[1])
        if url in self.url_to_title_and_date_map:
            title = self.url_to_title_and_date_map[url][0]
            title = title.strip()
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%d-%m-%Y"

    def get_date(self, response) -> str:
        url = unquote(response.url.rsplit("/", 1)[1])
        if url in self.url_to_title_and_date_map:
            date = self.url_to_title_and_date_map[url][1]
            date = date.replace("/", "-")
            date = date.strip()
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]
        return []

    def get_next_page(self, response)->str:
        return None