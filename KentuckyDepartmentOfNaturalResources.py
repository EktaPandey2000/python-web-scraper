import json
import re
from scraper.utils import helper
from scraper.OCSpider import OCSpider

class KentuckyDepartmentOfNaturalResources(OCSpider):
    name = 'KentuckyDepartmentOfNaturalResources'
    language = 'English'
    country = 'US'

    start_urls_names = {
           'https://newsroom.ky.gov/_layouts/15/Fwk.Webparts.Agency.Ui/ActivityStream/GetActivities.ashx?callback=jQuery11240977881795008922_1740046272504&PageIndex=0&Agencies=Kentucky+Energy+and+Environment+Cabinet&SearchText=&Category=&ShowDateAsHeader=true':''
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
        try:
            jsonp_text = response.text
            match = re.search(r'^[^(]*\((.*)\)\s*;?\s*$', jsonp_text)
            if not match:
                return []
            json_str = match.group(1)
            data = json.loads(json_str)
        except (json.JSONDecodeError, AttributeError) as e:
            return []
        articles = []
        results = data.get("Results", [])
        for result in results:
            items = result.get("Items", [])
            for item in items:
                link = item.get("LinkUrl")
                if link:
                    articles.append(link)
        return articles

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        #https://kydep.wordpress.com/2025/02/04/winners-of-the-2024-jim-claypool-art-and-conservation-writing-contest-announced/
        title = response.xpath("//h1[@class='entry-title']//text()").get()
        if not title:
            #https://landairwater.me/2025/01/08/kentucky-river-keepers-jamie-ponder/
            title = response.xpath("//h1[@class='title']//text()").get()
        title = title.replace('\xa03', '').replace('\xa0', '')
        return title.strip()

    def get_body(self, response) -> str:
        #https://kydep.wordpress.com/2025/02/04/winners-of-the-2024-jim-claypool-art-and-conservation-writing-contest-announced/
        body = response.xpath("//div[@class='entry-content']/p//text()").extract()
        if body==[]:
            #https://landairwater.me/2025/01/08/kentucky-river-keepers-jamie-ponder/
            body = response.xpath("//section[@class='entry']/p//text()").extract()
        body = helper.body_normalization(body,delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        pattern = r'/(\d{4}/\d{1,2}/\d{1,2})/'
        match = re.search(pattern, response.url)
        if match:
            date = match.group(1)
            date=date.replace('/','-')
            return date

    def get_images(self, response) -> list:
        images = []
        #https://kydep.wordpress.com/2025/02/04/winners-of-the-2024-jim-claypool-art-and-conservation-writing-contest-announced/
        image=response.xpath("//div[@class='entry-content']//img/@src").getall()
        if image==[]:
            #https://landairwater.me/2025/01/08/kentucky-river-keepers-jamie-ponder/
            image = response.xpath("//section[@class='entry']//@src").getall()
        for img in image :
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        #https://landairwater.me/2025/01/08/kentucky-river-keepers-jamie-ponder/
        author=response.xpath("//section[@class='entry']/p/text()").get()
        if not author:
            #https://kydep.wordpress.com/2025/03/20/kentucky-solar-for-all-meeting-april-3/
            author = response.xpath("//span[@class='author vcard']/a/text()").get()
        return [author]

    def get_next_page(self, response) -> str:
        match = re.search(r'(PageIndex=)(\d+)', response.url)
        if match:
            current_page = int(match.group(2)) + 1
            next_page_url = re.sub(r'(PageIndex=\d+)', f'PageIndex={current_page}', response.url)
            return next_page_url
        return None