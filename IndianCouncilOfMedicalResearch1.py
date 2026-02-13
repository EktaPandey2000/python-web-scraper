from scraper.OCSpider import OCSpider
# 1(T1)
class IndianCouncilOfMedicalResearch1(OCSpider):
    name = "IndianCouncilOfMedicalResearch1"
    source= "IndianCouncilOfMedicalResearch"
    country= "India"
    language= "English"
    charset = "iso-8859-1"
    exclude_rules = ["https://www.icmr.gov.in/icmrobject/custom_data/pdf/MERA-India-Newsletter/test"]

    start_urls_names = {
        "https://www.icmr.gov.in/mera-india-newsletter":""
    }

    start_urls_with_no_pagination_set = {
        "https://www.icmr.gov.in/mera-india-newsletter"
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
        article_links = response.xpath(".//div[@class='mediaCard__item-content title-main']/a[contains(@href, '.pdf')]/@href").getall()
        title_links = response.xpath("//div[@class='mediaCard__item-content title-main']/a[not(contains(@href, '.pdf'))and not(contains(@href, '/MERA-India-Newsletter/test'))and not(contains(text(), 'Issue 16, February 2022')) ]/text()").getall()
        if len(title_links) != len(article_links):
            print("response.url is not Matching the title to the article_links ", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/", 1)[1]] = [title_links[i]]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url=response.url.rsplit("/",1)[1]
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
        return "%B-%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1]
        if url in self.url_to_title_map:
            date = self.url_to_title_map[url][0]
            date = date.replace("Issue", "").strip()
            date= f"{date.split()[1]}-{date.split()[2]}"
            return date
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response)->str:
        return None