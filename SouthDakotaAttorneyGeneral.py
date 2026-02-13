from typing import Optional
from scraper.OCSpider import OCSpider
from scraper.utils.helper import body_normalization
from datetime import datetime 
from typing import Optional
import re

class SouthDakotaAttorneyGeneral(OCSpider):
    name = "SouthDakotaAttorneyGeneral"
    
    country = "US"

    start_urls_names = {
        "https://atg.sd.gov/OurOffice/Media/pressreleases.aspx": "Press Releases",
        }

    proxy_country = "us"

    custom_settings = {
        "DOWNLOADER_MIDDLEWARES":
            {
                'scraper.middlewares.GeoProxyMiddleware': 350,
            },
        "DOWNLOAD_DELAY": 2,
    }
    
    charset = "utf-8"
    
    visited_links = set()  # Keep track of visited URLs to avoid reprocessing
    
    @property
    def language(self): 
        return "English"

    @property
    def source_type(self) -> str:
        return "ministry"
    
    @property
    def timezone(self):
        return "America/Chicago"
    
    def get_articles(self, response) -> list:
        return response.xpath('//table[@id="pressrelease"]//h2/a/@href').getall()
    
    def get_href(self, entry) -> str:
        return entry
    
    def get_title(self, response) -> str:
        return response.xpath('//article[@class="cke_focus"]//span[@id="lbl_Title"]/text()').get()
    
    def get_body(self, response) -> str:
        return body_normalization(response.xpath('//article[@class="cke_focus"]//span[@id="lbl_HTML"]/*[not(strong[contains(text(), "FOR IMMEDIATE RELEASE:")])]').getall()) 
        
    def get_images(self, response) -> list:
        return response.xpath('//article[@class="cke_focus"]//span[@id="lbl_Img"]/img/@src').getall()
    
    def date_format(self) -> str:
        return"%m-%d-%Y"
    
    def get_date(self, response) -> Optional[str]:
        date_text = response.xpath('//span[@id="lbl_HTML"]/p[1]//text()').get()
        if not date_text or "FOR IMMEDIATE RELEASE" in date_text:
            date_text = response.xpath('//span[@id="lbl_HTML"]/p//text()[contains(., ", 202")]').get()
        if not date_text or "FOR IMMEDIATE RELEASE" in date_text:
            return None
        date_text = re.sub(r'\s+', ' ', date_text.replace("\xa0", " ")).strip()
        date_text = re.sub(r'(?i)FOR IMMEDIATE RELEASE[: ]*', '', date_text).strip()
        # Convert abbreviated months to full names
        month_map = {"Jan.": "January", "Feb.": "February", "Mar.": "March", "Apr.": "April", 
                    "May": "May", "Jun.": "June", "Jul.": "July", "Aug.": "August", 
                    "Sep.": "September", "Oct.": "October", "Nov.": "November", "Dec.": "December"}
        for abbr, full in month_map.items():
            date_text = date_text.replace(abbr, full)
        return datetime.strptime(date_text, "%A, %B %d, %Y").strftime("%m-%d-%Y")
        
    def get_authors(self, response):
        return []
    
    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> Optional[str]:
        return None   