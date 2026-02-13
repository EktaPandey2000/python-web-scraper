from scraper.OCSpider import OCSpider
from urllib.parse import unquote
# 14(T2)
class EnvironmentCentral14(OCSpider):
    name = "EnvironmentCentral14"
    source = "EnvironmentCentral"
    country = "India"
    language = "Hindi"
    charset = "iso-8859-1"
    exclude_rules = ["https://moef.gov.in/storage/tender/1757515231_Consultant%20(Admin.).pdf"]

    start_urls_names = {
        "https://moef.gov.in/whats-new/update":''
    }

    start_urls_with_no_pagination_set = {
        "https://moef.gov.in/whats-new/update"
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
        datetime_strs = response.xpath("//tbody//td[3]//text()").getall()
        article_links = response.xpath("//tbody//td//a//@href").getall()
        title_links = response.xpath("//tbody//tr//a/text()[1]").getall()
        if len(title_links) != len(article_links) or len(datetime_strs) != len(article_links):
            print("response.url is not matching the date and title to the article_links:", response.url)
            return []
        for i in range(len(article_links)):
            filename = unquote(article_links[i].rsplit("/", 1)[1])
            self.url_to_title_and_date_map[filename] = [datetime_strs[i], title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = unquote(response.url.rsplit("/", 1)[1])
        if url in self.url_to_title_and_date_map:
            return self.url_to_title_and_date_map[url][1]
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y-%m-%d"

    def get_date(self, response) -> str:
        url = unquote(response.url.rsplit("/", 1)[1])
        if url in self.url_to_title_and_date_map:
            date = self.url_to_title_and_date_map[url][0]
            return date.replace("/", "-")
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]
        return []

    def get_next_page(self, response) -> str:
        return None