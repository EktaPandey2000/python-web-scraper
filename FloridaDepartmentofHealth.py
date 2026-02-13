from scraper.utils import helper
from scraper.OCSpider import OCSpider

#https://www.floridahealth.gov/newsroom/2022/09/20220928-hurricane-ian.redirect.html
#https://www.floridahealth.gov/newsroom/2024/08/20240800-data-breach.redirect.html
#https://www.floridahealth.gov/newsroom/2023/06/20230626-mosquito.redirect.html
class FloridaDepartmentOfHealth(OCSpider):
    name = 'FloridaDepartmentOfHealth'
    language = 'English'
    country = 'US'

    start_urls_names = {
        'https://www.floridahealth.gov/newsroom/all-articles.html':''
    }

    default_article_xpath = "//ul[@class='article_list']//a"

    website_xpath = {
        'https://www.floridahealth.gov/newsroom/all-articles.html': default_article_xpath
    }

    HEADLESS_BROWSER_WAIT_TIME = 10000

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES": {
            # this middleware uses a headless browser to fetch the content
            'scraper.middlewares.HeadlessBrowserProxy': 350,
        }
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/New_York"

    start = 0
    end_counter = 90
    batch_size = 90
    skip_article_fetch = False
    articles_links = []
    def get_articles(self, response):
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
        title=response.xpath("//div[@class='headline']//h1//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body=response.xpath("//div[@id='article']//text()[not(ancestor::style) and not(ancestor::script)]").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//div[@class='headline']//p[@class='date']//text()").get()
        if(date is not None):
            date = date.split()
            date[1] = date[1][:-1]
            date = f"{date[0]}-{date[1]}-{date[2]}"
        return date

    def get_images(self, response) -> list:
        images = []
        image=response.xpath("//div[@id='article']//img/@src").getall()
        for img in image:
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