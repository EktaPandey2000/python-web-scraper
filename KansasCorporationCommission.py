from scraper.utils import helper
from scraper.OCSpider import OCSpider
from datetime import date
import requests
from bs4 import BeautifulSoup

class KansasCorporationCommission(OCSpider):
    name = 'KansasCorporationCommission'
    language = 'English'
    country = 'US'

    current_date = date.today()
    current_year = current_date.strftime("%Y")

    start_urls_names = {
                            f'https://www.kcc.ks.gov/commission-activity/news-releases/{current_year}':''
                        }

    default_article_xpath = "//div[@itemprop='articleBody']//p//a"

    website_xpath = {
                        f'https://www.kcc.ks.gov/commission-activity/news-releases/{current_year}': default_article_xpath
                    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Chicago"

    url_to_title_map= {}

    def get_articles(self, response) -> list:
        # https://www.kcc.ks.gov/news-10-30-23 (article title is inside a different tag and not mentioned, I took the landing page)
        # https://www.kcc.ks.gov/news-03-03-25
        article_links = response.xpath("//div[@itemprop='articleBody']//p//a//@href").getall()
        title_links = response.xpath("//div[@itemprop='articleBody']//p//a//text()").getall()
        if len(title_links) != len(article_links) :
            print("response.url is not Matching the title to the article_links", response.url)
            return []
        for i in range(len(article_links)):
            self.url_to_title_map[article_links[i].rsplit("/",1)[-1]] = title_links[i]
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = ''
        url = response.url.rsplit("/", 1)[-1]
        if (url in self.url_to_title_map):
            title = self.url_to_title_map[url]
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@itemprop='articleBody']//text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%Y-%B-%d'

    def get_date(self, response) -> str:
        date=response.xpath("//div[@itemprop='articleBody']//p[2]//text()").get()
        month, day, year= date.replace(",",'').split()
        date = f"{year}-{month}-{day}"
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@itemprop='articleBody']//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        #Every year has only 1 page
        base_url,year=response.url.rsplit("/",1)
        year=int(year)-1
        new_url=f"{base_url}/{year}"
        responses = requests.get(new_url)
        if responses.status_code == 200:
            soup = BeautifulSoup(responses.text, "html.parser")
            ul_tag = soup.find("div", itemprop="articleBody")
            if ul_tag:
                first_link = ul_tag.find("a")
                if first_link:
                    return new_url
        return None