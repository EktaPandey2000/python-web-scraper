from scraper.OCSpider import OCSpider
#2(T2)
class NewAndRenewableEnergyCentral2(OCSpider):
    name = "NewAndRenewableEnergyCentral2"
    source = "NewAndRenewableEnergyCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://mnre.gov.in/archive/":""
    }

    start_urls_names_with_no_pagination_set = {
        "https://mnre.gov.in/archive/"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_and_date_map= {}
    def get_articles(self, response) -> list:
        article_links = response.xpath("//span[@class='pdf-downloads']/a[1]/@href").getall()
        title = response.xpath("//tbody/tr/td[1]//a/text()").getall()
        date = response.xpath("//tbody/tr/td[2]//text()").getall()
        if(len(title) != len(article_links)) or (len(date) != len(article_links)):
            print("response.url is not Matching the date and title to the article_links", response.url)
            return[]
        for i in range(len(article_links)):
            self.url_to_title_and_date_map[article_links[i].rsplit("/", 1)[1]] = [date[i], title[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
        if url in self.url_to_title_and_date_map:
            title=self.url_to_title_and_date_map[url][1]
            return title
        return ""

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
        return ""

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None