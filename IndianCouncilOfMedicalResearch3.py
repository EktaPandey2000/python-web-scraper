from urllib.parse import urljoin
from scraper.OCSpider import OCSpider
import re
#3(T1)
class IndianCouncilOfMedicalResearch3(OCSpider):
    name = "IndianCouncilOfMedicalResearch3"
    source = "IndianCouncilOfMedicalResearch"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.icmr.gov.in/annual-accounts":""
    }

    start_url_with_no_pagination = {
        "https://www.icmr.gov.in/annual-accounts"
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
        articles = []
        for row in response.xpath("//div[@class='card']//table//tbody/tr"):
            title = row.xpath(".//td[2]//text()").get()
            url = row.xpath(".//td[3]//a[1]/@href").get()
            if not (title and url):
                continue
            full_url = urljoin(response.url, url)
            filename = full_url.rsplit("/", 1)[1]
            title = title.strip()
            self.url_to_title_map[filename] = [title]
            articles.append(full_url)
        return articles

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        title = response.url.rsplit("/", 1)[1]
        if title in self.url_to_title_map:
            title = self.url_to_title_map[title][0]
            title= title.strip()
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            title = self.url_to_title_map[url][0]
            match = re.search(r'(\d{4})[-_](\d{2,4})', title)
            if match:
                start, end = match.groups()
                if len(end) == 2:
                    end = start[:2] + end
                return start
            match = re.search(r'(\d{4})', title)
            if match:
                return match.group(1)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response):
        return None