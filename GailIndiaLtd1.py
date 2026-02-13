from scraper.OCSpider import OCSpider
import re
from urllib.parse import quote, unquote
#1(T3)
class GailIndiaLtd1(OCSpider):
    name = "GailIndiaLtd1"
    source = "GailIndiaLtd"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.gailonline.com/CSRIndex.html":""
    }

    start_url_with_no_pagination = {
        "https://www.gailonline.com/CSRIndex.html"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "SOE"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_map = {}
    def get_articles(self, response) -> list:
        article_links = response.xpath("//table[@class='table table-striped']//tr/td[1]//a/@href").getall()
        fy_pattern = r'FY\s*(\d{2,4})'
        ddmmyyyy_pattern = r'(\d{2})(\d{2})(\d{4})$'
        for link in article_links:
            link = link.strip()
            filename = link.rsplit("/", 1)[1].strip()
            encoded_filename = quote(filename)
            decoded_filename = unquote(encoded_filename)
            title = decoded_filename.replace(".pdf", "").replace("pdf", "")
            match = re.search(fy_pattern, title, re.IGNORECASE)
            if match:
                fy_start = match.group(1)
                if len(fy_start) == 2:
                    fy_start = "20" + fy_start
                date = fy_start
            else:
                fallback = re.search(r'\b(\d{4})\b', title)
                if fallback:
                    date = fallback.group(1)
                else:
                    ddmmyyyy_match = re.search(ddmmyyyy_pattern, title)
                    if ddmmyyyy_match:
                        date = ddmmyyyy_match.group(3)
                    else:
                        date = None
            self.url_map[encoded_filename] = [date, title]
        return article_links

    def get_href(self, entry) -> str:
        return f"https://www.gailonline.com/{quote(entry)}"

    def get_title(self, response) -> str:
        url = response.url.rsplit("/", 1)[1].strip()
        encoded_url = quote(unquote(url))
        if encoded_url in self.url_map:
            return self.url_map[encoded_url][1]
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str:
        url = response.url.rsplit("/", 1)[1].strip()
        encoded_url = quote(unquote(url))
        return self.url_map.get(encoded_url, [None, ""])[0]

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None