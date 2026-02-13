from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime
import scrapy

class WestVirginiaDepartmentOfTransportation(OCSpider):
    name = "WestVirginiaDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://transportation.wv.gov/" : "News"
    }
    
    def parse_intermediate(self, response):
        start_url = response.meta.get("start_url")
        current_year = response.meta.get("current_year", datetime.now().year)
        url = f"{start_url.rstrip('/')}/communications/PressRelease/Pages/{current_year}-Releases.aspx"
        def fallback_request():
            # Fall back to previous year if current year page doesn't exist
            previous_year = current_year - 1
            fallback_url = f"{start_url.rstrip('/')}/communications/PressRelease/Pages/{previous_year}-Releases.aspx"
            self.logger.warning(f"Fallback to {previous_year} due to 404 on current year")
            return scrapy.Request(
                url=fallback_url,
                callback=self.parse,
                dont_filter=True,
                meta={"start_url": start_url, "current_year": previous_year}
            )
        # Try the URL, fallback if 404
        yield scrapy.Request(
            url=url,
            callback=self.parse,
            dont_filter=True,
            meta={"start_url": start_url, "current_year": current_year},
            errback=lambda failure: fallback_request()
        )

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
    
    def get_articles(self, response) :
        return response.xpath('//a[contains(text(),"read more")]/@href').getall()
    
    def get_href(self, entry: str) -> str:
        return entry

    def get_title(self, response) :
        return response.xpath('//div[@class="container-fluid p-4"]//h1//text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//div[@id="articleContent"]//p//text()').getall())

    def get_images(self, response) :
        return response.xpath('//div[@id="articleContent"]//p//img/@src').getall()

    def date_format(self) -> str:
        return "%m/%d/%Y"

    def get_date(self, response) -> str:
        return response.xpath('//div[@id="articleDate"]//text()').get().strip()
    
    def get_authors(self, response) :
        return ""
    
    def get_page_flag(self) -> bool:
        return False
    
    def get_next_page(self, response):
        if response.status != 200 or "404" in response.url:
            self.logger.info("Invalid response or 404 page, stopping pagination.")
            return None
        current_year = int(response.meta.get("current_year"))
        return current_year - 1
    
    def go_to_next_page(self, response, start_url, current_page=None):
        start_url = response.meta.get("start_url")
        previous_year = self.get_next_page(response)
        if previous_year:
            url=f"{start_url}/communications/PressRelease/Pages/{previous_year}-Releases.aspx"
            self.logger.info(f"Next page URL: {url}")
            yield scrapy.Request(
                url = url,
                callback=self.parse_intermediate,
                meta = {
                    "start_url":start_url,
                    "current_year":previous_year
                }
            )
        else:
            self.logger.info("No more pages to scrape")
            return None