from scraper.OCSpider import OCSpider
#10(T2)
class EnvironmentCentral10(OCSpider):
    name = "EnvironmentCentral10"
    source = "EnvironmentCentral"
    country = "India"
    language = "Hindi"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://moef.gov.in/national-green-tribunal-ngt":''
    }

    start_urls_with_no_pagination_set = {
        "https://moef.gov.in/national-green-tribunal-ngt"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_map = {}
    def get_articles(self, response) -> list:
        article_links = response.xpath("//tbody//td//a//@href").getall()
        for link in article_links:
            link = link.strip()
            title = link.rsplit("/", 1)[1].replace(".pdf", "")
            date= link.split("/")
            date = f"{date[2]}-{date[3]}"
            self.url_map[link.rsplit("/", 1)[1]] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
        return f"https://moef.gov.in{entry}"

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_map:
            title = self.url_map[url][1]
            return title
        return None

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
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None