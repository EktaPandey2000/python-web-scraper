from scraper.OCSpider import OCSpider
import re
#8(T1)
class DepartmentOfPharmaceuticalsCentral8(OCSpider):
    name = "DepartmentOfPharmaceuticalsCentral8"
    source = "DepartmentOfPharmaceuticalsCentral"
    country = "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = [   #exclude rules for 'https://www.pharma-dept.gov.in/policy'
        "https://www.pharma-dept.gov.in/sites/default/files/UCMPMD_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/UCPMP%202024%20for%20website.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/"
        "DoP%20OM%20Dated%2005122022%20reg%20Establishing%20of%20EPC-MD_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/10.7.2023%20DoCA.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/Notification%20-%20R%26D%20Policy.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/OM%20dated%205-8-2022_Reconstitution%20of%20NMDPC%20unde"
        "r%20chairpersonship%20of%20Secretary%2C%20DoP_0.pdf",
        #exclude rules for "https://www.pharma-dept.gov.in/schemes"
       "https://www.pharma-dept.gov.in/sites/default/files/Final%20guidelines%20for%20SMDI-8.11.2024.pdf",
        "https://smdi.lsssdc.in",
        "https://www.pharma-dept.gov.in/sites/default/files/Approved%20Operational%20Guidelines%20%20%28PRIP%29.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/Tender%20notice_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/meeting%20notice_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/FAQ-PTUAS_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/FAQ-APICF_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/Corrigendum_4.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/FAQs%20in%20respect%20of%20RPTUAS%20-%20Copy.pdf",
        "20Guidelines%20for%20the%20Scheme%20Promotion%20of%20Medical%20Device%20Parks_0.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/Website%20updation%202022%20PMBJP-1.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/Guidelines%20for%20opening%20of%20new%20PMBJK.pdf",
        "https://www.pharma-dept.gov.in/sites/default/files/CAPPM%20-%20Guidekubes-current.pdf"
    ]

    start_urls_names = {
        "https://www.pharma-dept.gov.in/policy":"",
        "https://www.pharma-dept.gov.in/schemes":""
    }

    start_urls_with_no_pagination_set = {
        "https://www.pharma-dept.gov.in/policy",
        "https://www.pharma-dept.gov.in/schemes"
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
        article_links = response.xpath("//table[@class='views-table cols-3']//tbody//tr//a//@href").getall()
        title_links = response.xpath("//table[@class='views-table cols-3']//tbody//tr//a//text()").getall()
        if len(title_links) != len(article_links):
            print( "response.url is not Matching the title to the article_links ",response.url,)
            return []
        for link, title in zip(article_links, title_links):
            file_name = link.rsplit("/", 1)[1]
            title=title.strip()
            self.url_to_title_map[file_name] = [link, title]
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str | None:
        file_name = response.url.rsplit("/", 1)[1]
        if file_name in self.url_to_title_map:
            return self.url_to_title_map[file_name][1]
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str | None:
        file_name = response.url.rsplit("/", 1)[1]
        if file_name in self.url_to_title_map:
            title = self.url_to_title_map[file_name][1]
            pattern = r"(\d{4})"
            match = re.search(pattern, title)
            if match:
                return match.group(1)
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]

    def get_next_page(self, response) -> str:
        return None