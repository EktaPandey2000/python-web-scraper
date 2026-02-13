import re
from scraper.OCSpider import OCSpider
#3(T2)
class NewAndRenewableEnergyCentral3(OCSpider):
    name = "NewAndRenewableEnergyCentral3"
    source= "NewandRenewableEnergyCentral"
    country= "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://mnre.gov.in/en/blacklisted-company/":""
    }

    start_url_with_no_pagination={
        "https://mnre.gov.in/en/blacklisted-company/"
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
        article_links = response.xpath("//div[@class='wpb_wrapper']//ul//li//a/@href").getall()
        title_links = response.xpath("//div[@class='wpb_wrapper']//ul//li//text()[1]").getall()
        if (len(title_links) != len(article_links) ):
            print("response.url is not Matching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

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
        return "%Y-%m-%d"

    def get_date(self, response) -> str:
        date = response.url
        match = re.search(r'(20\d{2}(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01]))', date)
        if match:
            date = match.group(1)
            date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
            return date

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None