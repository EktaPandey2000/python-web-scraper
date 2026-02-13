import re
from datetime import date
import requests
from bs4 import BeautifulSoup
from scraper.utils import helper
from scraper.OCSpider import OCSpider

class GovernorOfDelaware(OCSpider):
    name = 'GovernorOfDelaware'
    language = 'English'
    country = 'US'

    current_date = date.today()
    current_year = current_date.strftime("%Y")
    current_month = current_date.strftime("%m")

    start_urls_names = {
            f'https://news.delaware.gov/{current_year}/{current_month}/page/1/':''
    }

    default_article_xpath = "(//div[@id='main_content'])[2]//h3//a"

    website_xpath = {
          f'https://news.delaware.gov/{current_year}/{current_month}/page/1/': default_article_xpath
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
        title = response.xpath("(//header[@class='pull-left'])[2]//h1/text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("(//div[@id='main_content'])[2]//text()").extract()
        body = helper.body_normalization(body,delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        date = response.url
        if date is not None:
            pattern = r'\d{4}/\d{2}/\d{2}'
            match = re.search(pattern, date)
            if match:
                date = match.group()
                date = date.replace('/','-')
        return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("(//div[@id='main_content'])[2]//img/@src").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
       return []

    def get_next_page(self, response):
        url = response.url.rstrip("/")
        parts = url.split("/")
        try:
            year = int(parts[3])
            month = int(parts[4])
            if "page" in parts:
                page_number = int(parts[-1])
            else:
                page_number = 1
        except (IndexError, ValueError) as e:
            return None

        next_page = page_number + 1
        if next_page == 1:
            next_page_url = f"https://news.delaware.gov/{year:04d}/{month:02d}/1/"
        else:
            next_page_url = f"https://news.delaware.gov/{year:04d}/{month:02d}/page/{next_page}/"
        response = requests.get(next_page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            div_tag = soup.find("div", id="main_content")
            if div_tag and div_tag.find("h3"):
                print("next_page_url",next_page_url)
                return next_page_url
        month -= 1
        if month == 0:
            year -= 1
            month = 12
        next_page_url = f"https://news.delaware.gov/{year:04d}/{month:02d}/"
        response = requests.get(next_page_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            div_tag = soup.find("div", id="main_content")
            if div_tag and div_tag.find("h3"):
                print("----next_page_url", next_page_url)
                return next_page_url
        return None