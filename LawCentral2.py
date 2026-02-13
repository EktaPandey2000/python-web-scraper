from scraper.OCSpider import OCSpider
#2(T1)
class LawCentral2(OCSpider):
    name = "LawCentral2"
    source= "LawCentral"
    country= "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://doj.gov.in/latest-orders-of-appointment-transfer-etc/":""
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
        article_links = response.xpath("//tbody//tr//td[1]//a/@href").getall()
        title = response.xpath("//tbody//tr//td[1]//a/text()").getall()
        if (len(title) != len(article_links) ):
            print("response.url is not Matching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [article_links[i] , title[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            title = self.url_to_title_map[url][1]
            title = title.split("(")[0]
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y-%m-%d"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            date = self.url_to_title_map[url][0]
            date= date.rsplit("/",1)[1].replace(".pdf","")
            date= f"{date[:4]}-{date[4:6]}-{date[6:8]}"
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        url = response.url
        if url.endswith("-etc/"):
            url = url.replace("-etc/", "-etc/page/2/")
        else:
            base_url = url.rsplit("/", 2)[0]
            page = url.rsplit("/", 2)[1]
            page = int(page) + 1
            url = f"{base_url}/{page}/"
        return url