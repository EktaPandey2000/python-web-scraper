from scraper.OCSpider import OCSpider
import re
#2[T3]
class IndianDrugManufacturersAssociation2(OCSpider):
    name = "IndianDrugManufacturersAssociation2"
    source = "IndianDrugManufacturersAssociation"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://idma-assn.org/ucpmp/guideline":'',
        "https://idma-assn.org/publication/annual_publication":''
    }

    start_url_with_no_pagination = {
        "https://idma-assn.org/ucpmp/guideline",
        "https://idma-assn.org/publication/annual_publication"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "industry_association"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_map = {}
    def get_articles(self, response) -> list:
        article_links = response.xpath(
            "//div[contains(@class, 'width_one ttt dpco')]//a/@href | //div[@class='process-item']/a[1]/@href").getall()
        titles = response.xpath(
            "//div[contains(@class, 'width_one ttt dpco')]//a/text() | //div[@class='process-item']/a[1]/h4/text()").getall()
        if len(titles) != len(article_links):
            self.logger.error(f"Mismatch between titles and links on {response.url}")
            return []
        pattern = r'\b(\d{4})\b'
        for link, title in zip(article_links, titles):
            title = title.strip()
            match = re.search(pattern, title)
            year_str = match.group(1) if match else None
            absolute_link = response.urljoin(link)
            self.url_to_title_map[absolute_link] = [title, year_str]
        return [response.urljoin(link) for link in article_links]

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url
        if url in self.url_to_title_map:
            return self.url_to_title_map[url][0]
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%Y"

    def get_date(self, response) -> str | None:
        url = response.url
        if url in self.url_to_title_map:
            return self.url_to_title_map[url][1]
        return None

    def get_authors(self, response):
        return []

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]
        return None

    def get_next_page(self, response) -> str:
        return None