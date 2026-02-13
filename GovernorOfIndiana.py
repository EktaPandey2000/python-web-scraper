from scraper.utils import helper
from scraper.OCSpider import OCSpider

class GovernorOfIndiana(OCSpider):
    name = 'GovernorOfIndiana'
    language = 'English'
    country = 'US'

    HEADLESS_BROWSER_WAIT_TIME = 50000

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                # for using geo targeted proxy, add this middleware
                'scraper.middlewares.HeadlessBrowserProxy': 350,
            },
        "DOWNLOAD_DELAY": 5,
    }

    start_urls_names = {
           'https://www.in.gov/gov/newsroom/news-releases/':''
    }

    default_article_xpath = "//section[@id='content_container_894533']//a"

    website_xpath = {
          'https://www.in.gov/gov/newsroom/news-releases/': default_article_xpath
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
        title = response.xpath("//h1[@class='em-header-card_title']//text()").getall()
        title = ' '.join(title)
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='em-content_about']//text()").extract()
        body = helper.body_normalization(body,delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//p[@class='em-date']//text()").get()
        if date is not None:
            date = date.split()
            date[2] = date[2][:-1]
            date = f"{date[1]}-{date[2]}-{date[3]}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='em-content_about']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
       return []

    def get_next_page(self, response) -> str:
            return None # no pagination required