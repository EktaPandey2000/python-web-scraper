from scraper.OCSpider import OCSpider
# 5(T2)
class NewAndRenewableEnergyCentral5(OCSpider):
    name = "NewAndRenewableEnergyCentral5"
    source= "NewAndRenewableEnergyCentral"
    country= "India"
    language= "English"
    charset = "iso-8859-1"

    HEADLESS_BROWSER_WAIT_TIME = 5000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            'scraper.middlewares.HeadlessBrowserProxy': 350,
        },
        "DOWNLOAD_DELAY": 3,
    }

    start_urls_names = {
        "https://mnre.gov.in/en/other-report/":""
    }

    start_urls_with_no_pagination_set = {
        "https://mnre.gov.in/en/other-report/"
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
        datetime_strs = response.xpath("//tbody//tr//td[@data-th='Date ']//span//text()").getall()
        article_links = response.xpath("//tbody//span[@class='pdf-downloads']//a[@class='download']/@href").getall()
        title_links = response.xpath("//tbody//tr//td[@data-th='Title ']//a/text()").getall()
        if len(title_links) != len(article_links) or len(datetime_strs) != len(article_links):
            print("response.url is not Matching the date and title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_and_date_map[article_links[i].rsplit("/", 1)[1]] = [datetime_strs[i], title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_title_and_date_map:
            title= self.url_to_title_and_date_map[url][1]
            title=title.strip()
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
            date = self.url_to_title_and_date_map[url][0]
            date=date.replace("/","-")
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None