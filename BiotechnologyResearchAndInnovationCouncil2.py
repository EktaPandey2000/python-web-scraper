from scraper.OCSpider import OCSpider
from urllib.parse import urlencode
import scrapy
from datetime import datetime
from scraper.utils import helper
#2[T3]
class BiotechnologyResearchAndInnovationCouncil2(OCSpider):
    name = 'BiotechnologyResearchAndInnovationCouncil2'
    source = 'BiotechnologyResearchAndInnovationCouncil'
    language = "English"
    country = 'India'
    charset = 'ISO-8859-1'
    """
       Examples of articles_without_title_body_media:
       # https://instem.res.in/events/diwali-deepavali/
       # https://instem.res.in/events/mahavir-jayanti/
       # https://instem.res.in/events/vinayak-chathurthi-ganeshchathurthi/
       # https://instem.res.in/publication/a-question-of-lineage/
     # https://instem.res.in/publication/genetic-testing-of-cardiomyopathies-position-statement-of-the-cardiological-society-of-india/
       """

    start_urls_names = {
        "https://instem.res.in/publication/":''
    }

    def parse_intermediate(self, response):
        current_page = response.request.meta.get("current_page", 1)
        payload = {
            'action': 'filter_posts',
            'paged': str(current_page),
            'category': 'all',
            'date': 'all',
            'order': 'desc',
        }
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://instem.res.in/publication/"
        }

        request = scrapy.Request(
            url=response.url,
            method="POST",
            body=urlencode(payload),
            headers=headers,
            callback=self.parse,
            dont_filter=True
        )
        request.meta["start_url"] = response.request.meta.get("start_url", response.url)
        request.meta["current_page"] = current_page
        yield request

    def get_page_flag(self) -> bool:
        return True

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "Asia/Kolkata"

    scraper_all_article = False
    def get_articles(self, response) -> list:
        article_links = response.css("a.publication__card-item::attr(href)").getall()
        print("article_links: ",article_links,len(article_links))
        return article_links

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='single-title']//h1/text()").get()
        return title.strip() if title else None

    def get_body(self, response) -> str:
        body= response.xpath("//div[@class='entry-content']//p//text()").getall()
        body = helper.body_normalization(body, delimiter="\n")
        return body

    def date_format(self) -> str:
        return "%Y-%m-%d"

    def get_date(self, response) -> str:
        date_str = response.xpath("//div[@class='single-top-section']//div[@class='date'][1]/p/text()").get()
        if date_str:
            date_obj = datetime.strptime(date_str.strip(), "%B %d, %Y")
            return date_obj.strftime(self.date_format())

    def get_images(self, response):
        return []

    def get_authors(self, response):
        return response.xpath("//div[@class='single-authors']//div[@class='single-tag']/text()").getall()

    def get_document_urls(self, response, entry=None):
        if response.url.lower().endswith(".pdf") or response.url.lower().endswith(".docx"):
            return [response.url]

    def go_to_next_page(self, response, start_url, current_page=None):
        current_page = response.request.meta.get("current_page", 1)
        next_page_number = current_page + 1
        request = response.request.replace(url=start_url, callback=self.parse_intermediate, dont_filter=True)
        request.meta['start_url'] = start_url
        request.meta["current_page"] = next_page_number
        yield request