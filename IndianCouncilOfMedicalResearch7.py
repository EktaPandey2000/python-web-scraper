from datetime import datetime
import logging
from scraper.OCSpider import OCSpider
import re
#7(T1)
class IndianCouncilOfMedicalResearch7(OCSpider):
    name = "IndianCouncilOfMedicalResearch7"
    source = "IndianCouncilOfMedicalResearch"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.nin.res.in/newsletter.html": ""
    }

    start_urls_names_with_no_pagination_set = {
        "https://www.nin.res.in/newsletter.html"
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
    def get_articles(self, response) -> list:
        article_links = response.xpath("//tbody/tr/td[3]/a/@href").getall()
        titles = response.xpath("//tbody/tr/td//b/text()").getall()
        dates = response.xpath("//tbody/tr/td[1]//text()").getall()
        if (len(titles) != len(article_links)) or (len(dates) != len(article_links)):
            print("response.url is not Matching the title and date to the article_links", response.url)
            return []
        for i, href in enumerate(article_links):
            full_url = response.urljoin(href)
            self.url_to_title_and_date_map[full_url] = [dates[i].strip(), titles[i].strip()]
        return list(self.url_to_title_and_date_map.keys())

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url
        if url in self.url_to_title_and_date_map:
            return self.url_to_title_and_date_map[url][1]
        logging.debug("No title found for %s", url)
        return ""

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%d-%B-%Y"

    def get_date(self, response) -> str:
        url = response.url
        raw_date = ""
        if url in self.url_to_title_and_date_map:
            raw_date = self.url_to_title_and_date_map[url][0].strip()
        if not raw_date:
            logging.warning("No date found for %s, using run_date", url)
            return self.run_date.strftime("%d-%B-%Y")
        raw_date = ' '.join(raw_date.split())
        raw_date = raw_date.replace("/", "-").replace(",", "")
        if re.fullmatch(r"[A-Za-z]+[- ]\d{4}", raw_date):
            raw_date = "01-" + raw_date.replace(" ", "-")
        for fmt in ("%d-%B-%Y", "%d %B %Y", "%B-%Y", "%B %Y"):
            try:
                dt = datetime.strptime(raw_date, fmt)
                return dt.strftime("%d-%B-%Y")
            except ValueError:
                continue
        logging.warning("Unparsed date %r for %s, using run_date", raw_date, url)
        return self.run_date.strftime("%d-%B-%Y")

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if any(ext in response.url.lower() for ext in (".pdf", ".doc", ".docx")):
            return [response.url]
        return []

    def get_next_page(self, response) -> str:
        return None