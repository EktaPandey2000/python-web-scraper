from scraper.utils import helper
from scraper.OfficialLineSpider import configure_ol_spider
from scraper.OCSpider import OCSpider
import re

class OfficeoftheComptrolleroftheCurrencyOCC(OCSpider):
    name = 'OfficeoftheComptrolleroftheCurrencyOCC'
    language = 'English'
    country = 'US'

    start_urls_names = {
        'https://www.occ.gov/news-events/newsroom/?q=&nr=NewsRelease&topic=&dte=0&stf=0&rpp=10':''
    }

    default_article_xpath = "//a[@class='focus-title']"

    website_xpath = {
        'https://www.occ.gov/news-events/newsroom/?q=&nr=NewsRelease&topic=&dte=0&stf=0&rpp=10': default_article_xpath
    }

    custom_settings = configure_ol_spider()

    HEADLESS_BROWSER_WAIT_TIME = 10000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            # this middleware uses a headless browser to fetch the content
            'scraper.middlewares.HeadlessBrowserProxy': 350,
        },
        "DOWNLOAD_DELAY": 3,

    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/New_York"

    def get_articles(self, response) -> list:
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//main[@id='main_content']/h1/text()").get()
        return title.strip()

    def get_document_urls(self, response, entry=None):
        return [response.urljoin(i) for i in response.xpath(
                "//section[@class='occgov-section__content-subsection occgov-issuance-content']//a//@href").extract() if
                '.pdf' in i]

    def get_body(self, response) -> str:
        body = response.xpath(
            "//section[@class='occgov-section__content-subsection occgov-issuance-content']//text()").extract()
        body = helper.body_normalization(body, delimiter='')
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//span[@class='date']/text()").get()
        if (date is not None):
            date = date.replace(" ", "-").replace(",", "")
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath(
                "//section[@class='occgov-section__content-subsection occgov-issuance-content']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        match = re.search(r"stf=(\d+)", response.url)
        if match:
            stf_value = int(match.group(1)) + 10
            if(stf_value in [60]):
                stf_value+=10
            next_url = re.sub(r"stf=\d+", f"stf={stf_value}", response.url)
            return next_url
        return None