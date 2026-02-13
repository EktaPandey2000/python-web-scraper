from scraper.OCSpider import OCSpider
# 3(T2)
class EnvironmentCentral3(OCSpider):
    name = "EnvironmentCentral3"
    source= "EnvironmentCentral"
    country= "India"
    language= "Hindi"
    charset = "iso-8859-1"
    exclude_rules = ["https://moef.gov.in/storage/tender/1723024218.pdf"]

    start_urls_names = {
        "https://moef.gov.in/esa-notifications":""
    }

    start_urls_with_no_pagination_set = {
        "https://moef.gov.in/esa-notifications/"
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
    all_article_links = []
    batch_size = 90
    scraper_all_article = False
    def get_articles(self, response) -> list:
        if not self.scraper_all_article:
            article_links = response.xpath("//td//a/@href").getall()
            title_links = response.xpath("//td//a/text()").getall()
        if (len(title_links) != len(article_links)):
            print("Mismatching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [title_links[i], article_links[i]]
        self.all_article_links.extend(article_links)
        return self.all_article_links[:self.batch_size]

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url= response.url.rsplit("/",1)[1]
        if url in self.url_to_title_map:
            title= self.url_to_title_map[url][0]
            title=title.strip()
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
        if url in self.url_to_title_map:
            date = self.url_to_title_map[url][1]
            date = date.rsplit("/", 1)[0].replace("/uploads/", "").replace("/","-")
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