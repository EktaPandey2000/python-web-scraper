from scraper.OCSpider import OCSpider
import re
# 9(T1)
class IndianCouncilOfMedicalResearch9(OCSpider):
    name = "IndianCouncilOfMedicalResearch9"
    source= "IndianCouncilOfMedicalResearch"
    country= "India"
    language= "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.nin.res.in/scientific.html":""
    }

    start_urls_with_no_pagination_set = {
        "https://www.nin.res.in/scientific.html"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_date_map = {}
    def get_articles(self, response) -> list:
        article_links = response.xpath("//tr//td/a/@href").getall()
        date_links = response.xpath("//tr//td/a/text()").getall()
        if len(date_links) != len(article_links):
            print("response.url is not Matching the date to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_date_map[article_links[i].rsplit("/", 1)[1]] = [date_links[i] , article_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_date_map:
            title= self.url_to_date_map[url][1]
            title = title.replace("scientific/", "").replace(".pdf", "")
            title = title.strip()
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
        if url in self.url_to_date_map:
            date = self.url_to_date_map[url][0]
            pattern = r"\b(\d{4})(?:-(\d{4}))?\b"
            match = re.search(pattern, date)
            if match:
                return match.group(2) if match.group(2) else match.group(1)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None