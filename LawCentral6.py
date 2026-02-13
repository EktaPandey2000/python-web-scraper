from scraper.OCSpider import OCSpider
#6(T1)
class LawCentral6(OCSpider):
    name = "LawCentral6"
    source = "LawCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://legalaffairs.gov.in/documents/list-law-officers":''
    }

    start_urls_with_no_pagination_set = {
        "https://legalaffairs.gov.in/documents/list-law-officers"
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
        article_links = response.xpath("//span[@class='file']//a//@href").getall()
        for link in article_links:
            link = link.strip()
            title = link.rsplit("files/", 1)[1].replace("%20", " ").replace(".pdf", "")
            date = title.rsplit("ASG",1)[-1].replace(".","-").strip()
            self.url_map[link.rsplit("/", 1)[1]] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
        return entry

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
        return "%d-%m-%Y"

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