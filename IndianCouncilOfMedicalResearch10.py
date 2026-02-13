from urllib.parse import urljoin
from scraper.OCSpider import OCSpider
from datetime import datetime
import re
#10(T1)
class IndianCouncilOfMedicalResearch10(OCSpider):
    name = "IndianCouncilOfMedicalResearch10"
    source = "IndianCouncilOfMedicalResearch"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    HEADLESS_BROWSER_WAIT_TIME = 1000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350,
        },
        "DOWNLOAD_DELAY": 1,
    }

    start_urls_names = {
        "https://www.nin.res.in/tenders.html": ""
    }

    start_url_with_no_pagination = {
        "https://www.nin.res.in/tenders.html"
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
        article_links = response.xpath(
            "//div[contains(@class,'update-text')]//a[not(contains(@href,'#')) "
            "and (contains(@href,'.pdf') or contains(@href,'.doc') or contains(@href,'.docx'))]/@href").getall()
        title_links = response.xpath(
            "//div[contains(@class,'update-text')]//a[not(contains(@href,'#')) "
            "and (contains(@href,'.pdf') or contains(@href,'.doc') or contains(@href,'.docx'))]/text()").getall()
        datetime_strs = response.xpath(
            "//div[contains(@class,'update-text')]//h4[normalize-space(text()) != '' and string-length(normalize-space(text())) > 0]/text()").getall()
        article_links = [a.strip() for a in article_links]
        title_links = [t.strip() for t in title_links]
        datetime_strs = [d.strip() for d in datetime_strs]
        if len(article_links) != len(title_links):
            print("Warning: titles and links length mismatch", response.url)
        for i, link in enumerate(article_links):
            key = link.rsplit("/", 1)[-1]
            date = datetime_strs[i] if i < len(datetime_strs) else ""
            title = title_links[i]
            self.url_to_title_and_date_map[key] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_and_date_map:
            title = self.url_to_title_and_date_map[url][1]
            if title:
                return title.strip()
        title = response.xpath(
            "//h4[normalize-space(text()) != '' and string-length(normalize-space(text())) > 0]/text()").get()
        if title:
            return title.strip()
        return "Untitled"

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%B-%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_and_date_map:
            raw_date = self.url_to_title_and_date_map[url][0].strip()
            if raw_date:
                for fmt in ["%B %Y", "%d-%m-%Y"]:
                    try:
                        return datetime.strptime(raw_date, fmt).strftime(self.date_format())
                    except ValueError:
                        continue
                return datetime.today().strftime(self.date_format())
            else:
                return datetime.today().strftime(self.date_format())
        return datetime.today().strftime(self.date_format())

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]

    def go_to_next_page(self, response, start_url, current_page=None):
        return None