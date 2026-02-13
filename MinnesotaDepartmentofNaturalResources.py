from scraper.utils import helper
from scraper.OCSpider import OCSpider

class MinnesotaDepartmentofNaturalResources(OCSpider):
    name = 'MinnesotaDepartmentofNaturalResources'
    language = 'English'
    country = 'US'

    start_urls_names = {
        'https://www.dnr.state.mn.us/news/index.html?page=0':''
    }

    default_article_xpath = "//h3[@class='field-content']//a"

    website_xpath = {
        'https://www.dnr.state.mn.us/news/index.html?page=0': default_article_xpath
    }

    proxy_country = "us"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                # for using geo targeted proxy, add this middleware
                'scraper.middlewares.GeoProxyMiddleware': 350,
            },
        "DOWNLOAD_DELAY": 2,
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Chicago"

    def get_articles(self, response) -> list:
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='row news_article']//h1//span//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='content']//p//text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//section[@id='main_page_content']//p//text()").get()
        date = date.replace(", "," ").replace(" ","-")
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='content']//img//@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        web,page = response.url.split("?page=")
        next_page = int(page)+1
        return f'{web}?page={next_page}'