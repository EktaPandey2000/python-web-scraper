from scraper.utils import helper
from scraper.OCSpider import OCSpider
from datetime import date
import re

class DelawareDivisionOfPublicHealth(OCSpider):
    name = 'DelawareDivisionOfPublicHealth'
    language = 'English'
    country = 'US'
    charset='ISO-8859-1'

    current_date = date.today()
    current_year = int(current_date.strftime("%Y"))

    start_urls_names = {
        "https://www.dhss.delaware.gov/dhss/pressreleases/pressrel.html":'',
        f"https://www.dhss.delaware.gov/dhss/pressreleases/{current_year-1}/pressrel.html":''
    }

    default_article_xpath = "//li[@class='dblspace']//a"

    website_xpath = {
        "https://www.dhss.delaware.gov/dhss/pressreleases/pressrel.html":default_article_xpath,
        f'https://www.dhss.delaware.gov/dhss/pressreleases/{current_year-1}/pressrel.html': default_article_xpath,
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/New_York"

    article_links = []
    batch_size = 90
    def get_articles(self, response) -> list:
        articles = response.xpath(self.website_xpath.get(response.meta.get('start_url')))
        self.article_links.extend(articles)
        return self.article_links[:self.batch_size]

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title=response.xpath("//h2//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='container']//p[not(ancestor::div[@class='row show-grid']) and not(ancestor::div[@class='row'])] //text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def date_format(self) -> str:
        return '%m-%d-%Y'

    def get_date(self, response) -> str:
        months_dict = {
            "01": "January",
            "02": "February",
            "03": "March",
            "04": "April",
            "05": "May",
            "06": "June",
            "07": "July",
            "08": "August",
            "09": "September",
            "10": "October",
            "11": "November",
            "12": "December",
        }
        #https://www.dhss.delaware.gov/dhss/pressreleases/2024/acsnlcsd_103124.html(October 31, 2023)
        date = response.xpath("//span[@class='b'][text()='Date:']/following-sibling::text()[1]").get()
        if (date is not None):
            date = date.replace(",", "").strip().split()
            date[0] = next(num for num, names in months_dict.items() if date[0].capitalize() in names)
            #https://www.dhss.delaware.gov/dhss/pressreleases/2018/houstondog_02212018.html(February, 2018)
            if len(date)<3:
               date= response.url.rsplit("_")[1].split(".")[0]
               day=date[:2]
               month=date[2:4]
               year=date[4:]
               if(len(year)==4):
                   date=f"{day}-{month}-{year}"
                   return date
               #https://www.dhss.delaware.gov/dhss/pressreleases/2018/callcent_060118.html(June, 2018)
               else:
                   year="20"+year
                   date=f"{day}-{month}-{year}"
                   return date
            date = f"{date[0]}-{date[1]}-{date[2]}"
            return date

    def get_images(self, response) -> list:
        images = []
        for img in response.xpath("//div[@class='container']//img/@src[not(ancestor::div[@class='row'])]").getall():
            if ('.png' in img) or ('.jpg' in img):
                images.append(response.urljoin(img))
        return images

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        match = re.search(r'(\d{4})', response.url)
        if match:
            current_year = int(match.group(1))
            next_year = current_year - 1
            next_url = response.url.replace(str(current_year), str(next_year))
            return next_url

    def go_to_next_page(self, response, start_url, current_page=None):
        url=self.get_next_page(response)
        if len(self.article_links):
            self.article_links=self.article_links[self.batch_size:]
            request = response.request.replace(url=url,callback=self.parse)
            request.meta['start_url'] = start_url
            yield request
        else:
            yield None