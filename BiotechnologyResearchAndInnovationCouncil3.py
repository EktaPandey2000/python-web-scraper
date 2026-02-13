from scraper.utils import helper
from scraper.OCSpider import OCSpider
#3[T3]
class BiotechnologyResearchAndInnovationCouncil3(OCSpider):
    name = 'BiotechnologyResearchAndInnovationCouncil3'
    source = 'BiotechnologyResearchAndInnovationCouncil'
    language = "English"
    country = 'India'
    charset = 'ISO-8859-1'
    """
    Examples of articles_without_title_body_media:
    https://instem.res.in/events/amr-research-conference-arc-2025/
    https://instem.res.in/events/sage-2025/
    https://instem.res.in/events/vinayak-chathurthi-ganeshchathurthi/
    https://instem.res.in/events/vinayak-chathurthi-ganeshchathurthi/
    https://instem.res.in/events/diwali-deepavali/
    """

    start_urls_names = {
      "https://instem.res.in/events/":''
    }

    start_url_with_no_pagination_set = {
        "https://instem.res.in/events/"
    }

    default_article_xpath = "//div[@class='wrap']//h3//a"

    website_xpath = {
        'https://instem.res.in/events/':default_article_xpath
    }

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "Asia/Kolkata"

    def get_articles(self, response) -> list:
        return response.xpath(self.website_xpath.get(response.meta.get('start_url')))

    def get_href(self, entry) -> str:
        return entry.attrib['href']

    def get_title(self, response) -> str:
        title = response.xpath("//div[@class='wrap']/h1/text()").get()
        return title.strip()

    def get_body(self, response) -> str:
        body = response.xpath("//div[@class='entry-content active']//text()").extract()
        body = helper.body_normalization(body, delimiter=" ")
        return body

    def get_images(self, response) -> list:
        images = []
        for img in  response.xpath("//img[@class='alignnone wp-image-6280 size-full']//@src").getall():
            if ('.png' in img) or ('.jpg' in img) or ('.src' in img):
                images.append(response.urljoin(img))
        return images

    def date_format(self) -> str:
        return '%d-%B-%Y'

    def get_date(self, response) -> str:
        date = response.xpath("//div[@class='date']/text()").get()
        date = date.rsplit(",")[1].strip().replace(" ","-")
        return date

    def get_authors(self, response):
        return []

    def get_document_urls(self, response, entry=None):
        if ".pdf" in response.url.lower() or ".doc" in response.url.lower() or ".docx" in response.url.lower():
            return [response.url]

    def get_next_page(self, response) -> str:
        return None