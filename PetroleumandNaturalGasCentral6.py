from scraper.OCSpider import OCSpider
#6(T2)
class PetroleumandNaturalGasCentral6(OCSpider):
    name = "PetroleumandNaturalGasCentral6"
    source = "PetroleumAndNaturalGasCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://mopng.gov.in/en/page/21":""
    }

    start_urls_with_no_pagination_set = {
        "https://mopng.gov.in/en/page/21"
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
        articles = []
        for i in response.xpath("//tbody//tr"):
            url = i.xpath(".//td[2]//a/@href").get()
            title = i.xpath(".//td[1]//text()").get()
            date = i.xpath(".//td[3]//text()").get()
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
        return f"https://mopng.gov.in/{entry}"

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
        return "%d-%m-%Y"

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
        return None