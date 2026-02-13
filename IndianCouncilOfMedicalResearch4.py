from scraper.OCSpider import OCSpider
import re
import urllib.parse
import logging
#4(T1)
class IndianCouncilOfMedicalResearch4(OCSpider):
    name = "IndianCouncilOfMedicalResearch4"
    source = "IndianCouncilOfMedicalResearch"
    country = "India"
    language = "English"
    charset = "iso-8859-1"
    exclude_rules = [
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/Executive_Summary_in_Hindi.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/DelayStatementHindi.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/Delay_Statement_English.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/1720340891_executive_summary_in_hindi.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/ExecutiveSummary_English.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/AR_Hindi.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/ICMR_AR_Hindi.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/ICMR_AR_English.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/ICMR_AnnualReport_English_2007_08.pdf',
    'https://www.icmr.gov.in/icmrobject/custom_data/pdf/annual-reports/ICMR_AR_English%202014-15%20final%20pdf.pdf'
    ]

    start_urls_names = {
        "https://www.icmr.gov.in/annual-reports":'',
    }

    start_urls_with_no_pagination_set = {
        "https://www.icmr.gov.in/annual-reports"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_map = {}
    def get_articles(self, response) -> list:
        links = response.xpath("//table[@class='table table-bordered']//tbody//td//a[1]//@href").getall()
        pattern = r'(19\d{2}|20\d{2})'
        for link in links:
            link = link.strip()
            decoded_link = urllib.parse.unquote(link)
            title = decoded_link.rsplit("/", 1)[-1].replace(".pdf", "").strip()
            match = re.search(pattern, title)
            date = match.group(1) if match else None
            self.url_map[decoded_link.rsplit("/", 1)[1]] = [date, title]
        return links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = urllib.parse.unquote(response.url).rsplit("/", 1)[1]  # decode %20
        if url in self.url_map:
            return self.url_map[url][1]
        logging.warning(f"[ICMR Spider] Title not found for URL: {response.url}")
        return ""

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str:
        url = urllib.parse.unquote(response.url).rsplit("/", 1)[1]  # decode %20
        if url in self.url_map:
            return self.url_map[url][0]
        return None

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in [".pdf", ".doc", ".docx"]):
            return [response.url]

    def get_next_page(self, response) -> str:
        return None