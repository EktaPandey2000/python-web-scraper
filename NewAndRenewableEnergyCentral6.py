from scraper.OCSpider import OCSpider
#6(T2)
class NewAndRenewableEnergyCentral6(OCSpider):
    name = 'NewAndRenewableEnergyCentral6'
    source = "NewAndRenewableEnergyCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://mnre.gov.in/whats-new/":''
    }

    start_urls_with_no_pagination_set = {
        "https://mnre.gov.in/whats-new/"
    }

    default_article_xpath = "//div[@class='wpb_wrapper']//ul/li/a"

    website_xpath = {
        'https://mnre.gov.in/whats-new/': default_article_xpath
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "Asia/Kolkata"

    def get_articles(self, response) -> list:
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='row']//h1/text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        return ""

    def date_format(self) -> str:
        return '%d-%m-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//tbody//tr//td[2]//text()").get()
        if date:
            date = date.strip()
            date = date.replace("/", "-")
            return date

    def get_images(self, response) -> list:
        return []

    def get_authors(self, response):
        return []

    def get_document_urls(self, response, entry=None):
        return [i for i in response.xpath("//tbody//tr//td[1]//a/@href").getall()
                if i.lower().endswith(".pdf")]

    def get_next_page(self, response) -> str:
        return None