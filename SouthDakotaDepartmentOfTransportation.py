from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class SouthDakotaDepartmentOfTransportation(OCSpider):
    name = "SouthDakotaDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://dot.sd.gov/inside-sddot/media/press-releases": "Press Releases"
    }
    
    charset="utf-8"

    @property
    def language(self) -> str:
        return "English"
    
    @property
    def source_type(self) -> str:
        return "ministry"

    @property
    def timezone(self) -> str:
        return "US/Eastern"
    
    article_to_date_mapping ={}  # Mapping date with articles from start URL
    
    def get_articles(self, response) :
        mapping = {}
        articles_urls =[]
        entries = response.xpath('//div[@class="blogs"]//a[@class="blogPostListing"]')
        for article in entries:
            url = article.xpath(".//@href").get()
            full_url = response.urljoin(url)
            articles_urls.append(full_url)
            date = article.xpath('.//div[@class="blogPostListingDate"]/text()').get()
            if url and date :
                mapping[full_url] = date
        self.article_to_date_mapping.update(mapping)
        return articles_urls
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) :
        return response.xpath('//h1[@class="h1Sub"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@class="umb-block-grid__layout-container"]//p/text()').getall())

    def get_images(self, response) :
        return []

    def date_format(self) -> str:
        return "%B %d, %Y"

    def get_date(self, response) -> str:
        article_url = response.url
        article_date = self.article_to_date_mapping.get(article_url, None)
        if article_date:
            return article_date
        else:
            self.logger.error(f"No date found for URL: {article_url}")
            return None
    
    def get_authors(self, response) :
        return []
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response) :
        return response.xpath('//a[contains(text(),"Next")]/@href').get()