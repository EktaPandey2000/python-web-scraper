from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization

class NevadaDepartmentOfTransportation(OCSpider):
    name = 'NevadaDepartmentOfTransportation'

    country = "US"

    HEADLESS_BROWSER_WAIT_TIME = 30000  #30 seconds wait time
    
    custom_settings = {
		"DOWNLOADER_MIDDLEWARES" : {
			'scraper.middlewares.HeadlessBrowserProxy': 350,
		},
		"DOWNLOAD_DELAY" : 5,
	}
    
    HEADLESS_BROWSER_WAIT_TIME = 30000 
    
    start_urls_names = {
        'https://www.dot.nv.gov/doing-business/news/news-releases': "News",
        'https://www.dot.nv.gov/doing-business/news/news-releases/-arch-1': "News"
    }

    charset = "utf-8"

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def language(self):
        return "English"

    @property
    def timezone(self):
        return "US/Central"

    def get_articles(self, response) -> list:
        articles = response.xpath("//h2//a//@href").getall()
        return [response.urljoin(link) for link in articles]
    
    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return response.xpath("//h2[@class='detail-title']//text()").get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath("//div[@class='detail-content']//p//text()").getall())
    
    def get_images(self, response) -> list:
        return []
    
    def date_format(self) -> str:
        return '%m/%d/%Y %I:%M %p'

    def get_date(self, response) -> str:
        return response.xpath("//div[@class='detail-list']//span[@class='detail-list-value']//text()").get(default="").strip()
        
    def get_authors(self, response):
        return ""

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        next_page = response.xpath("//div[@class='list-pager']//a[contains(text(),' Next » ')]//@href").get()
        if next_page:
            return response.urljoin(next_page) 
        else:
            return None