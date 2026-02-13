from scraper.OCSpider import OCSpider
#1(T2)
class EnvironmentCentral1(OCSpider):
    name = "EnvironmentCentral1"
    source= "EnvironmentCentral"
    country= "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://moef.gov.in/budget-details":""
    }

    start_url_with_no_pagination={
        "https://moef.gov.in/budget-details"
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
        article_links = response.xpath("//tbody//tr//td[2]//a/@href").getall()
        title_links = response.xpath("//tr//td//a/text()[1]").getall()
        if (len(title_links) != len(article_links) ):
            print("response.url is not Matching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return f"https://moef.gov.in{entry}"

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            title = self.url_to_title_map[url][0]
            title = title.split("(")[0]
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
            date = self.url_to_title_map[url][0]
            date = date.split()[-1].split("-")[0]
        return date

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None