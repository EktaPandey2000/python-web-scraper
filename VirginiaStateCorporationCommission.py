import re
from scraper.utils import helper
from scraper.OCSpider import OCSpider

class VirginiaStateCorporationCommission(OCSpider):
    name = 'VirginiaStateCorporationCommission'
    language = 'English'
    country = 'US'

    HEADLESS_BROWSER_WAIT_TIME = 10000

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                # for using geo targeted proxy, add this middleware
                'scraper.middlewares.HeadlessBrowserProxy': 350,
            },
        "DOWNLOAD_DELAY": 2,
    }

    start_urls_names = {
        'https://www.scc.virginia.gov/media/sccvirginiagov-home/site-assets/js/news.json?t=1743160219404':''
    }

    start_urls_with_no_pagination_set = {
        'https://www.scc.virginia.gov/media/sccvirginiagov-home/site-assets/js/news.json?t=1743160219404'
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
        data=response.text
        pattern = r'"shortName":"(.*?)"'
        shorturls = re.findall(pattern, data)
        return shorturls

    def get_href(self, entry) -> str:
        return f"https://www.scc.virginia.gov{entry}"

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='col-lg-8 mr-auto news-release-title']//h1//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body =  response.xpath("//div[@class='container']//text()").extract()
        body = helper.body_normalization(body,delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%b-%d-%Y'

    def get_date(self, response) -> str:
        date  = response.xpath("//div[@class='main-section--header']//p[@class='release-date']//text()").get()
        if date:
            date = date.split()
            date[1]=date[1][:-1]
            date = f"{date[0]}-{date[1]}-{date[2]}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='container']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
       return []

    def get_next_page(self, response) -> str:
        #No pagination is required
        return None