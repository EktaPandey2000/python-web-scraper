from scraper.OCSpider import OCSpider
#5(T2)
class PetroleumAndNaturalGasCentral5(OCSpider):
    name = "PetroleumAndNaturalGasCentral5"
    source = "PetroleumAndNaturalGasCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://mopng.gov.in/en/page/13":''
    }

    start_urls_with_no_pagination_set = {
        "https://mopng.gov.in/en/page/13"
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
        months = response.xpath("//table[@class='table table-bordered']/tbody/tr/td[3]/text()").getall()
        years = response.xpath("//table[@class='table table-bordered']/tbody/tr/td[2]/text()").getall()
        article_links = response.xpath("//table[@class='table table-bordered']/tbody/tr/td/a/@href").getall()
        if not (len(months) == len(years) == len(article_links)):
            print(" Mismatch in months/years/article_links count for", response.url)
            return []
        for i in range(len(article_links)):
            month = months[i].strip()
            year = years[i].strip()
            link = article_links[i].strip()
            title = link.rsplit("/",1)[1]
            title= title.replace(".pdf","")
            date = f"{month[:3]}-{year}"
            self.url_to_date_map[link.rsplit("/", 1)[1]] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
       return f"https://mopng.gov.in/{entry}"

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        return self.url_to_date_map.get(url, [None, None])[1]

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%b-%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_date_map:
            date = self.url_to_date_map[url][0]
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]

    def get_next_page(self, response) -> str:
        return None