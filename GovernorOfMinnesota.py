from bs4 import BeautifulSoup
from scraper.OCSpider import OCSpider
import json
from scraper.utils import helper
# https://mn.gov/governor/newsroom/press-releases/#/detail/appId/1/id/673920 (URL contains HashTag)
class GovernorOfMinnesota(OCSpider):
    name = 'GovernorOfMinnesota'
    language = 'English'
    country = 'US'

    start_urls_names = {
           'https://mn.gov/governor/rest/list/Newsroom?id=1055&nav=Date,Category,Tag&page=1,10&sort=Date,descending':''
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
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            return []
        records = data.get("list",[])
        ids = [{"id": article.get("id")}for article in records if "id" in article]
        return ids

    def get_href(self, entry) -> str:
        id = entry.get("id")
        return f"https://mn.gov/governor/rest/item/Newsroom?id=1055-{id}&nav=Date"

    def get_title(self, response) -> str:
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            return None
        title = data.get("item", {}).get("Title", "")
        return title.strip()

    def get_body(self, response) -> str:
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            return None
        article = data.get("item", {}).get("BodyText")
        soup = BeautifulSoup(article, 'html.parser')
        img_tags = soup.find_all('img')
        self.imageslist = [img.get('src') for img in img_tags]
        text_content = soup.get_text(separator=" ", strip=True)
        body_content = helper.body_normalization([text_content], delimiter=" ")
        return body_content

    def date_format(self) -> str:
        return '%Y-%m-%dT%H:%M:%S%z'

    def get_date(self, response) -> str:
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError as e:
            return None
        date = data.get("item", {}).get("Date")
        return date

    def get_images(self, response) -> list:
        image_list = []
        images = getattr(self, 'imageslist')
        for i in images:
            if (".png" in i.lower() or ".jpg" in i.lower()):
                image_list.append({i})
            return image_list
        return []

    def get_authors(self, response):
       return []

    def get_next_page(self, response) -> str:
        base_url = response.url.replace(",10&sort=Date,descending","")
        base_url=base_url.rsplit("=")[-1]
        next_page = int(base_url) + 1
        if(next_page in [75,77]):
            next_page+=1
        return f'https://mn.gov/governor/rest/list/Newsroom?id=1055&nav=Date,Category,Tag&page={next_page},10&sort=Date,descending'