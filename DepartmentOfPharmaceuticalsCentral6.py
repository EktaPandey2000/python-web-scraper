from scraper.OCSpider import OCSpider
import re
#6(T1)
class DepartmentOfPharmaceuticalsCentral6(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral6"
    source = "DepartmentOfPharmaceuticalsCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = ["www.pharma-dept.gov.in/sites/default/files/New%20Constitution%20Order%20dated%2021.06.2024.pdf",
                     "www.pharma-dept.gov.in/sites/default/files/Reforms%20in%20the%20Pricing%20Framework_0.pdf",
                     "20to%20prevent%20Sexual%20harassment%20of%20Women%20at%20workplace.pdf",
                     "https://www.pharma-dept.gov.in/sites/default/files/LPC.pdf",
                     "/Constitution%20of%20Standing%20Committee%20on%20Affordable%20Medicines.pdf"]

    start_urls_names = {
        "https://www.pharma-dept.gov.in/work-allocation-and-committees":''
    }

    start_url_with_no_pagination = {
        "https://www.pharma-dept.gov.in/work-allocation-and-committees"
    }

    HEADLESS_BROWSER_WAIT_TIME = 10000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 360,
        },
        "DOWNLOAD_DELAY": 2,
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
        article_links = response.xpath("//div[@class='view-content']//a//@href").getall()
        titles = response.xpath("//div[@class='scroll-table']//table//tbody//tr//td[2]/text()").getall()
        if len(titles) != len(article_links):
            print("response.url is not Matching the title to the article_links ", response.url, )
            return []
        pattern = r'(\d{4})'
        for link, title in zip(article_links, titles):
            title = title.strip()
            match = re.search(pattern, title)
            date = match.group(1) if match else None
            self.url_to_title_map[link] = [title, date]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url
        if url in self.url_to_title_map:
            return self.url_to_title_map[url][0]
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str | None:
        url = response.url
        if url in self.url_to_title_map:
            return self.url_to_title_map[url][1]
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None