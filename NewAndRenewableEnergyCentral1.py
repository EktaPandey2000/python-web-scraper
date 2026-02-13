from scraper.OCSpider import OCSpider
# 1(T2)
class NewAndRenewableEnergyCentral1(OCSpider):
    name = "NewAndRenewableEnergyCentral1"
    source="NewAndRenewableEnergyCentral"
    language= "English"
    country = "India"

    start_urls_names = {
        "https://mnre.gov.in/en/annual-report/":""
    }

    start_urls_with_no_pagination_set = {
        "https://mnre.gov.in/en/annual-report/"
    }

    default_article_xpath = "//ul//li[@style='background:#ef7f00']//a"

    website_xpath = {
        'https://mnre.gov.in/en/annual-report/':default_article_xpath
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
        title = response.xpath("//div[@class='col-lg-11 col-md-11 col-sm-11 col-xs-12']//h1//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        return ""

    def get_document_urls(self, response, entry=None):
        return [i for i in response.xpath("//div[@class='wpb_wrapper']//ul//li//a/@href").extract()
                if '.pdf' or '.doc' or '.docx' in i]

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        date_url= response.xpath("//div[@class='wpb_wrapper']//ul//li//a/@href").get()
        date_url = date_url.rsplit("/", 1)[1].replace(".pdf", "")
        date_year= date_url[:4]
        date_month= date_url[4:6]
        date_day= date_url[6:8]
        date= f"{date_year}-{date_month}-{date_day}"
        return date

    def get_images(self, response) -> list:
        return []

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        return None