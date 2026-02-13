from scraper.utils import helper
from scraper.OCSpider import OCSpider
from scraper.OfficialLineSpider import configure_ol_spider

# https://www.nmhealth.org/news/alert/2020/12/?view=1296 no title and date

class NewMexicoDepartmentofHealth(OCSpider):
    name = 'NewMexicoDepartmentofHealth'
    language = 'English'
    country = 'US'

    start_urls_names = {
                        'https://www.nmhealth.org/news/all/':''
    }

    default_article_xpath = "//div[@id='content']//table//tbody//tr//td//a"

    website_xpath = {
                        'https://www.nmhealth.org/news/all/':default_article_xpath
    }

    custom_settings = configure_ol_spider()
    HEADLESS_BROWSER_WAIT_TIME = 10000
    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                # for using geo targeted proxy, add this middleware
                'scraper.middlewares.HeadlessBrowserProxy': 350,
            },
        "DOWNLOAD_DELAY": 2,
    }
    exclude_rules = ["https://www.nmhealth.org/news/all/#top*"]

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Denver"

    articles_links = []
    start = 0
    end_counter  = 90
    batch_size = 90
    skip_article_fetch = False
    def get_articles(self, response) -> list:
        if not self.skip_article_fetch:
            articles= response.xpath(self.website_xpath.get(response.meta.get('start_url')))
            self.articles_links.extend(articles)
            self.skip_article_fetch = True
            return self.articles_links[self.start:self.end_counter]
        else:
            return self.articles_links[self.start:self.end_counter]

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//div[@id='content']//h1//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@id='content']//p//text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%Y-%B-%d'

    def get_date(self, response) -> str:
        date=response.xpath("//div[@class='newsDetails']//em//text()").get()
        month, day, year = date.replace(",",'').replace("- ",'').strip().split()
        date = f"{year}-{month}-{day}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@id='content']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def go_to_next_page(self, response, start_url, current_page=None):
        self.start = self.end_counter
        self.end_counter  = self.start + self.batch_size
        if self.start < len(self.articles_links):
            request = response.request.replace(url=response.url, callback=self.parse)
            request.meta['start_url'] = start_url
            yield request
        else:
            yield None