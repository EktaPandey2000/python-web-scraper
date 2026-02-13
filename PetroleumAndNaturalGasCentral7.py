from scraper.OCSpider import OCSpider
#7(T2)
class PetroleumAndNaturalGasCentral7(OCSpider):
    name = "PetroleumAndNaturalGasCentral7"
    source= "PetroleumAndNaturalGasCentral"
    country= "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = ["Projects_to_the_Nation.pdf"]

    start_urls_names = {
        "https://mopng.gov.in/en/psu-whats-new":""
    }

    start_urls_with_no_pagination_set = {
        "https://mopng.gov.in/en/psu-whats-new"
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
        datetime_strs = response.xpath("//ul[@class='commonListing']//p//text()").getall()
        article_links = response.xpath("//ul[@class='commonListing']//li/a/@href").getall()
        title_links = response.xpath("//ul[@class='commonListing']//li/a//text()").getall()
        if len(title_links) != len(article_links) or len(datetime_strs) != len(article_links):
            print("response.url is not Matching the date and title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_and_date_map[article_links[i].rsplit("/", 1)[1]] = [datetime_strs[i], title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return f"https://mopng.gov.in/{entry}"

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_title_and_date_map:
            title=self.url_to_title_and_date_map[url][1]
            return title
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%d-%m-%Y"

    def get_date(self, response, date=None) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_and_date_map:
            date=self.url_to_title_and_date_map[url][0]
            date = f"{date.split()[3]}-{date.split()[4]}-{date.split()[5]}"
            date = date.replace(",-", "-")
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None