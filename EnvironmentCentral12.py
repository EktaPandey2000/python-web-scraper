from scraper.OCSpider import OCSpider
#12(T2)
class EnvironmentCentral12(OCSpider):
    name = "EnvironmentCentral12"
    source = "EnvironmentCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://moef.gov.in/other-reports":""
    }

    start_urls_names_with_no_pagination_set = {
        "https://moef.gov.in/other-reports"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "Ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_map= {}
    def get_articles(self, response) -> list:
        article_links = response.xpath("//tbody//tr//td//a/@href").getall()
        for link in article_links:
            link = link.strip()
            title = link.rsplit("/", 1)[1].replace(".pdf", "")
            date = link.split("/")
            date = f"{date[2]}-{date[3]}"
            self.url_map[link.rsplit("/", 1)[1]] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
        return f"https://moef.gov.in{entry}"

    def get_title(self, response) -> str:
        url = response.url.rsplit("/",1)[1]
        if url in self.url_map:
            title=self.url_map[url][1]
            return title
        return ""

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y-%m"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_map:
            date = self.url_map[url][0]
            return date
        return ""

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None