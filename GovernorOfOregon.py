from scraper.utils import helper
from scraper.OCSpider import OCSpider

class GovernorOfOregon(OCSpider):
    name = 'GovernorOfOregon'
    language = 'English'
    country = 'US'

    start_urls_names = {
           'https://apps.oregon.gov/oregon-newsroom/or/Posts/Search?page=0':''
    }

    default_article_xpath = "//div[@class='col-md-9']/div/a"

    website_xpath = {
          'https://apps.oregon.gov/oregon-newsroom/or/Posts/Search?page=0': default_article_xpath
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Los_Angeles"

    def get_articles(self, response) -> list:
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='row'][2]/div[@class='col-md-8']/text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='row'][3]/div[@class='col-md-8']//text() | //div[@class='row'][4]/div[@class='col-md-8']//text()").extract()
        body = helper.body_normalization(body,delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%B-%d-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//div[@class='col-md-8']//span[last()]/a/text()").get()
        if date is not None:
            date = date.strip()
            date = date.split()
            date[1] = date[1][:-1]
            date = f"{date[0]}-{date[1]}-{date[2]}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='row text-center']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
       return []

    def get_next_page(self, response) -> str:
        base_url, current_page = response.url.split("?page=")
        next_page = int(current_page) + 1
        return f"{base_url}?page={next_page}"