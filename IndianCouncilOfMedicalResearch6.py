from scraper.OCSpider import OCSpider
#6(T1)
class IndianCouncilOfMedicalResearch6(OCSpider):
    name = "IndianCouncilOfMedicalResearch6"
    source = "IndianCouncilOfMedicalResearch"
    country = "India"
    language = "English"
    charset = "iso-8859-1"

    start_urls_names = {
        "https://www.nin.res.in/researchbrief.html":""
    }

    start_urls_names_with_no_pagination_set = {
        "https://www.nin.res.in/researchbrief.html"
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return "Ministry"

    @property
    def timezone(self):
        return "Asia/Kolkata"

    url_to_title_and_date_map = {}
    def get_articles(self, response) -> list:
        article_links = response.xpath('//tbody//tr//td[3]/a/@href').getall()
        titles = response.xpath("//tbody/tr/td[2][normalize-space()]//text()[normalize-space()]").getall()
        dates = response.xpath("//tbody/tr/td[1]/text()").getall()
        if (len(titles) != len(article_links)) or (len(dates) != len(article_links)):
            print("Mismatch between titles, dates, and links:", response.url)
            return []
        absolute_urls = []
        for i in range(len(article_links)):
            full_url = response.urljoin(article_links[i])
            self.url_to_title_and_date_map[full_url] = [dates[i].strip(), titles[i].strip()]
            absolute_urls.append(full_url)
        return absolute_urls

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        url = response.url
        if url in self.url_to_title_and_date_map:
            title = self.url_to_title_and_date_map[url][1]
            return ' '.join(title.split())
        return None

    def get_body(self, response) -> str:
        return ""

    def get_images(self, response) -> list:
        return []

    def date_format(self) -> str:
        return "%d-%B-%Y"

    def get_date(self, response) -> str:
        url = response.url
        if url.lower().endswith((".pdf", ".doc", ".docx")):
            return self.run_date.strftime("%d-%B-%Y")
        if url in self.url_to_title_and_date_map:
            raw_date = self.url_to_title_and_date_map[url][0].strip()
            return " ".join(raw_date.split())
        return self.run_date.strftime("%d-%B-%Y")

    def get_authors(self, response):
        return ""

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None