from scraper.OCSpider import OCSpider
from typing import List
import scrapy
import re
import chardet

class NewJerseyDepartmentOfTransportation(OCSpider):
    name = 'NewJerseyDepartmentOfTransportation'
     
    country = "US"

    start_urls_names = {
        'https://www.nj.gov/transportation/about/press/index_archive.shtml': "Press"
    }

    article_data_map = {}  # Mapping title and PDF with respective articles

    def parse_intermediate(self, response):
        all_articles = list(set(response.xpath("//div[@class='content']//h5//a//@href").getall()))
        total_articles = len(all_articles)
        articles_per_page = 100
        start_url = response.meta.get("start_url", response.url)
        for start_idx in range(0, total_articles, articles_per_page):  # Indexing for virtual pagination
            yield scrapy.Request(
                url=start_url,
                callback=self.parse,
                meta={
                    'start_idx': start_idx, 
                    'articles': all_articles, 
                    'start_url': start_url
                },
                dont_filter=True
            )

    charset = "iso-8859-1"

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
        try:
            articles_with_duplicate = response.xpath("//div[@class='content']")
            all_articles = set()
            for article in articles_with_duplicate:
                full_url = article.xpath(".//h5//a/@href").get()
                title = article.xpath(".//h5//a/text()").get()
                if full_url:
                    if not title:
                        title = response.xpath("//title/text()").get(default="").strip()
                    self.article_data_map[full_url] = {  # Mapping done for indexing
                        "title": title.strip(),
                        "pdf": [full_url],
                    }
                    all_articles.add(full_url)
            all_articles = list(all_articles)
            start_idx = response.meta.get('start_idx', 0)  # Indexing should be called from parse_intermediate only
            end_idx = min(start_idx + 100, len(all_articles))
            return all_articles[start_idx:end_idx]  # Only Article url's are extracted and returned
        except Exception as e:
            return []

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("title", "")

    def get_body(self, response) -> str:
        if ".pdf" not in response.url:
            try:
                detected = chardet.detect(response.body)
                encoding = detected.get('encoding') or self.charset
                content_type = response.headers.get('Content-Type', b'').decode('utf-8', 'ignore')
                if 'text' in content_type or 'html' in content_type:
                    body = response.body.decode(encoding, errors='ignore')
                    body = response.xpath("//table[@align='right']//td[@valign='top']//p//text()").getall()
                    return "\n".join([b.strip() for b in body if b.strip()])
            except Exception as e:
                return
        return ""

    def get_images(self, response) -> list:
        if ".pdf" not in response.url:
            try:
                content_type = response.headers.get('Content-Type', b'').decode('utf-8', 'ignore')
                if 'text' in content_type or 'html' in content_type:
                    images = response.xpath("//table[@align='right']//td[@valign='top']//p//img//@src").getall()
                    if images:
                        return [response.urljoin(img) for img in images]
            except Exception as e:
                return 
        return []

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        try:
            match = re.search(r"(\d{4})(\d{2})(\d{2})", response.url)
            if match:
                year, month, day = match.groups()
                return f"{year}-{month}-{day}"
            else:
                match = re.search(r"/(\d{2})(\d{2})(\d{2})", response.url)
                if match:
                    month, day, year = match.groups()
                    return f"20{year}-{month}-{day}"
        except Exception as e:
            self.logger.error(f"Failed to extract date: {e}")
        return None

    def get_authors(self, response):
        return []

    def get_document_urls(self, response, entry=None) -> List[str]:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("pdf", "")

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response) -> str:
        # No next page to scrape
        return None