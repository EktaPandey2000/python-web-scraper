from datetime import date
from bs4 import BeautifulSoup
from scraper.utils import helper
from scraper.OCSpider import OCSpider
import requests

class NewJerseyBoardofPublicUtilities(OCSpider):
    name='NewJerseyBoardofPublicUtilities'
    language='English'
    country = 'US'
    charset = 'ISO-8859-1'
    current_date = date.today()
    current_year = current_date.strftime("%Y")

    start_urls_names = {
        f'https://www.nj.gov/bpu/newsroom/{current_year}/approved/news_archive.html':''
    }

    default_article_xpath="//div[@class='content wide']//ul//li//a"

    website_xpath = {
        f'https://www.nj.gov/bpu/newsroom/{current_year}/approved/news_archive.html':default_article_xpath
    }

    exclude_rules = ["http:////nj.gov/*","https://nj.gov/*","http://www.nj.gov/*"]

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

    def get_document_urls(self, response, entry=None):
        if '.pdf' in response.url:
            return [i for i in response.xpath("//div[@class='content wide']//a//@href | //div[@class='col-sm-12']//a//@href | //div[@class='col-sm-12 newsmain']//a//@href |\
             //div[@class='node__content']//a//@href | //div[@class='l-sidebar__main']//a//@href").extract() if '.pdf' or 'docx' in i]

    def get_title(self, response) -> str:
        #https://www.nj.gov/bpu/newsroom/2018/approved/20181231.html
        title = response.xpath("//h2[@class='subTitle']//text()").get()
        if not title:
            #https://nj.gov/governor/news/news/562025/approved/20250131c.shtml
            title = response.xpath("//div[@class='row']//h3//text()").get()
        if not title:
            # https://dep.nj.gov/newsrel/22_0011/
            title = response.xpath("//h3[@class='col-sm-12 text-center']//text()").getall()
            title = title[0]
        if not title:
            #https://www.ntia.gov/press-release/2024/biden-harris-administration-approves-new-jersey-s-internet-all-initial-proposal
            title = response.xpath("//div[@class='page-title-not-front']//span//text()").get()
        if not title:
            #https://www.epa.gov/newsreleases/epa-156-million-grant-provide-solar-power-lower-energy-costs-and-advance-environmental
            title = response.xpath("//div[@class='l-sidebar__main']//h1//text()").get()
        return title.strip()

    def get_body(self, response) -> str:
            #https://www.nj.gov/bpu/newsroom/2018/approved/20181231.html
        body = response.xpath("//div[@class='content wide']//text()").extract()
        if not body:
          #https://nj.gov/governor/news/news/562025/approved/20250131c.shtml
            body = response.xpath("//div[@class='col-sm-12']//p//text()").extract()
        if not body:
            # https://dep.nj.gov/newsrel/22_0011/
            body = response.xpath("//div[@class='col-sm-12 newsmain']//section//text()").extract()
        if not body:
            #https://www.ntia.gov/press-release/2024/biden-harris-administration-approves-new-jersey-s-internet-all-initial-proposal
            body = response.xpath("//div[@class='node__content']//p//text()").extract()
        if not body:
            #https://www.epa.gov/newsreleases/epa-156-million-grant-provide-solar-power-lower-energy-costs-and-advance-environmental
            body = response.xpath("//div[@class='l-sidebar__main']//p//text()").extract()
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
            "12": "December"
        }
        #https://www.ntia.gov/press-release/2024/biden-harris-administration-approves-new-jersey-s-internet-all-initial-proposal (September 06, 2024)
        # https://www.epa.gov/newsreleases/epa-156-million-grant-provide-solar-power-lower-energy-costs-and-advance-environmental
        dates = response.xpath("//article[@class='article']//time//text() | //div[@class='field__item']//text()").get()
        if dates:
            dates = dates.replace(", ", " ")
            dates = dates.split(" ")
            if dates[0] in months_dict.values():
                month = next(num for num, name in months_dict.items() if name == dates[0])
                return f"{month}-{dates[1]}-{dates[2]}"
            else:
                return None
        else:
            # https://dep.nj.gov/newsrel/22_0011/
            dates = response.xpath("//div[@class='col-sm-6']//p//text()").getall()
            if dates:
                dates = dates[1].strip()
                dates = dates.replace(", ", " ")
                dates = dates.split(" ")
                month = next(num for num, name in months_dict.items() if name == dates[0])
                return f"{month}-{dates[1]}-{dates[2]}"
            else:
                # https://nj.gov/governor/news/news/562025/approved/20250131c.shtml (01/31/2025)
                dates = response.xpath("//div[@class='text-muted ']//text()").get()
                if dates:
                    if " - " in dates:
                        dates = dates.split(" - ")[1]
                        dates = dates.replace("/", "-")
                    else:
                        dates = dates.replace("/", "-")
                    return dates.strip()
                else:
                    #https://www.nj.gov/bpu/newsroom/2018/approved/20181231.html (12/31/2018)
                    dates = response.xpath("//table[@id='newsHeader']//td//text()").getall()
                    if dates:
                        dates = dates[-2].strip()
                        dates = dates.replace("/", "-")
                        return dates
                    else:
                        return None

    def get_images(self, response) -> list:
        images = []
        # https://www.nj.gov/bpu/newsroom/2018/approved/20181231.html
        # https://dep.nj.gov/newsrel/22_0011/
        # https://www.ntia.gov/press-release/2024/biden-harris-administration-approves-new-jersey-s-internet-all-initial-proposal
        xpath_names = ["//div[@class='content wide']//img//@src",
                       "//div[@class='col-sm-12 newsmain']//img//@src",
                       "//div[@class='node__content']//img//@src"]
        for xpath_name in xpath_names:
            for img in response.xpath(xpath_name).getall():
                if ('.png' in img) or ('.jpg' in img):
                    images.append(response.urljoin(img))
            if images:
                break
        return images

    def get_authors(self, response):
        return []

    def get_next_page(self, response) -> str:
        base_url,year,page,pages= response.url.rsplit("/", 3)
        year = int(year) - 1
        new_url = f"{base_url}/{year}/{page}/{pages}"
        new_url = str(new_url)
        responses = requests.get(new_url)
        if responses.status_code == 200:
            soup = BeautifulSoup(responses.text, "html.parser")
            ul_tag = soup.find("div", class_="content wide")
            if ul_tag:
                first_link = ul_tag.find("a")
                if first_link:
                    return new_url
        return None