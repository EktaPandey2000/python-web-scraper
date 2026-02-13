import scrapy
from scraper.middlewares import HeadlessBrowserProxy
from scraper.utils import helper
from scraper.OCSpider import OCSpider

class IllinoisDepartmentOfNaturalResources(OCSpider):
    name = 'IllinoisDepartmentOfNaturalResources'
    language = 'English'
    country = 'US'

    start_urls_names = {
        'https://dnr.illinois.gov/news/olderpressreleases2011on.html':''
    }

    default_article_xpath = "//div[@class='cmp-news-feed']//ul//li//a"

    website_xpath = {
        'https://dnr.illinois.gov/news/olderpressreleases2011on.html': default_article_xpath
    }

    def parse_intermediate(self, response):
        hbp = HeadlessBrowserProxy()
        request = scrapy.Request(hbp.get_proxy(response.url, timeout=40000), callback=self.parse)
        request.meta['start_url'] = response.request.meta['start_url']
        yield request

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Chicago"

    start = 0
    end_counter = 90
    batch_size = 90
    skip_article_fetch = False
    articles_links = []
    def get_articles(self, response) -> list:
        if not self.skip_article_fetch:
            articles = response.xpath(self.website_xpath.get(response.meta.get('start_url')))
            self.articles_links.extend(articles)
            self.skip_article_fetch = True
            return self.articles_links[self.start:self.end_counter]
        else:
            return self.articles_links[self.start:self.end_counter]

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//h1[@class='cmp-title__text']/text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='text']//div[@class='cmp-text ']//text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//span[@class='template__sub-title lable-font-style']/text()").get()
        if (date is not None):
            date = date.split()
            date = date[4:]
            date[1] = date[1][:-1]
            date = f"{date[0]}-{date[1]}-{date[2]}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='text']//div[@class='cmp-text ']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def go_to_next_page(self, response, start_url, current_page=None):
        self.start = self.end_counter
        self.end_counter = self.start + self.batch_size
        if self.start < len(self.articles_links):
            request = response.request.replace(url=response.url, callback=self.parse)
            request.meta['start_url'] = start_url
            yield request
        else:
            yield None