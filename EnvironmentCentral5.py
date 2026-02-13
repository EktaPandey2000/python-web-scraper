from scraper.OCSpider import OCSpider
#5(T2)
class EnvironmentCentral5(OCSpider):
    name = "EnvironmentCentral5"
    source = "EnvironmentCentral"
    country = "India"
    language = "Hindi"
    charset = "iso-8859-1"
    exclude_rules = ["Decision-of-127th-EC-Meeting.pdf", "/uploads/pdf-uploads/pdf_67e1515d08e867.44035473.pdf"]

    start_urls_names = {
        "https://moef.gov.in/importexport-of-hazardous-other-waste":''
    }

    start_url_with_no_pagination = {
        "https://moef.gov.in/importexport-of-hazardous-other-waste"
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
    all_article_links = []
    batch_size = 90
    scraper_all_article = False
    def get_articles(self, response) -> list:
        datetime_strs = response.xpath("//tbody//tr//td[3]/text()").getall()
        article_links = response.xpath("//tbody//tr//td//a[1]/@href").getall()
        title_links = response.xpath("//tr//td//a[1]/text()[1]").getall()
        if len(title_links) != len(article_links) or len(datetime_strs) != len(article_links):
            print("response.url is not Matching the date and title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_and_date_map[article_links[i].rsplit("/", 1)[1]] = [datetime_strs[i], title_links[i]]
        self.all_article_links.extend(article_links)
        return self.all_article_links[:self.batch_size]

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_and_date_map:
            title = self.url_to_title_and_date_map[url][1]
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
            date = date.replace("/", "-")
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def go_to_next_page(self, response, start_url, current_page=None):
        if len(self.all_article_links) > 0:
            self.all_article_links = self.all_article_links[self.batch_size:]
            request = response.request.replace(url=response.url, callback=self.parse)
            request.meta['start_url'] = start_url
            yield request
        else:
            return None