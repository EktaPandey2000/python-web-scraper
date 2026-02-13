from scraper.OCSpider import OCSpider
# 10(T1)
class DepartmentOfPharmaceuticalsCentral10(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral10"
    source="DepartmentOfPharmaceuticalsCentral"
    language= "English"
    country = "India"

    start_urls_names = {
        "https://www.pharma-dept.gov.in/whats-new?title=&page=0":""
    }

    default_article_xpath = "//div[@class='views-field views-field-title']//a"

    website_xpath = {
        'https://www.pharma-dept.gov.in/whats-new?title=&page=0':default_article_xpath
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
        title = response.xpath("//h1[@class='heading']//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        return ""

    def get_document_urls(self, response, entry=None):
        return [i for i in response.xpath("//span[@class='field-content']//a/@href").extract()
                if '.pdf' or '.doc' or '.docx' in i]

    def date_format(self) -> str:
        return '%d-%b-%Y'

    def get_date(self, response) -> str:
        date= response.xpath("//span[@class='lastupdated']//strong/text()").get()
        date = date.replace(" ","-")
        return date

    def get_images(self, response) -> list:
        return []

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        base_url, current_page = response.url.rsplit("=",1)
        next_page = int(current_page) + 1
        return f"{base_url}={next_page}"