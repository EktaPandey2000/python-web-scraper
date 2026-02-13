from scraper.OCSpider import OCSpider
import re
#3(T2)
class PetroleumAndNaturalGasCentral3(OCSpider):
    name = "PetroleumAndNaturalGasCentral3"
    source = "PetroleumAndNaturalGasCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = ["https://mopng.gov.in/files/Whatsnew/India&#039;s-Hydrocarbon-Outlook-Report---2023-2024.pdf"]

    start_urls_names = {
        "https://mopng.gov.in/en/home/whatsnew?page=1":""
    }

    def get_page_flag(self) -> bool:
        return True

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_and_date_map = {}
    def get_articles(self, response) -> list:
        articles = []
        for i in response.xpath("//tbody/tr"):
            url = i.xpath(".//td[@class='views-field views-field-php']//a/@href").get()
            title = i.xpath(".//td[@class='views-field views-field-title']//text()").get()
            date = i.xpath(".//span[@class='date-display-single']//text()").get()
            if not (url and title and date):
                continue
            if url and title and date:
                full_url = url.rsplit("/",1)[1]
                title = title.strip()
                clean_date = date.strip()
                self.url_to_title_and_date_map[full_url] = [title, clean_date]
                articles.append(url)
        return articles

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_title_and_date_map:
            title=self.url_to_title_and_date_map[url][0]
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%m-%d-%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_and_date_map:
            date = self.url_to_title_and_date_map[url][1]
            date=date.replace("/","-")
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        base_url, current_page = response.url.rsplit("=", 1)
        next_page = int(current_page) + 1
        return f"{base_url}={next_page}"