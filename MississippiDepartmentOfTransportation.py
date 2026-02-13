from scraper.OCSpider import OCSpider
import scrapy
import json
from typing import List

class MississippiDepartmentOfTransportation(OCSpider):
    name = "MississippiDepartmentOfTransportation"

    country = "US"

    start_urls_names = {
        "https://mdot.ms.gov/portal/news": "Press Releases",
    }

    api_start_url = {
        'https://mdot.ms.gov/portal/news': {
            'url': 'https://mdot.ms.gov/odata/t_news_release?$orderby=event_date desc&$top=20',
        }
    }
    
    def parse_intermediate(self, response):
        start_url = response.meta.get('start_url')
        api_data = self.api_start_url.get(start_url)
        payload = response.meta.get("payload", {"skip": 0})
        if not api_data or 'url' not in api_data:
            return
        api_url = f"{api_data['url']}&$skip={payload['skip']}"
        yield scrapy.Request(
            url=api_url,
            method="GET",
            callback=self.parse,
            meta={
                "start_url": start_url,
                "api_url": api_url,
                "payload": payload,
            },
            dont_filter=True
        )

    charset = "utf-8"
    
    article_data_map = {}  # Mapping title, date and body from Json of respective articles

    @property
    def language(self):
        return "English"

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "US/Central"

    def get_articles(self, response) -> list:
        try:
            content_type = response.headers.get('Content-Type').decode('utf-8')
            if 'application/json' in content_type:
                data = json.loads(response.text)
            else:
                return []
        except json.JSONDecodeError as e:
            return []
        if not data.get("value"):
            return []
        articles = []
        for item in data.get("value", []):
            news_id = item.get("news_id")
            if news_id:
                url = f'https://mdot.ms.gov/portal/news_release_view/{news_id}'
                title = item.get("title", "").strip()
                date = item.get("create_date", "").strip()
                body = item.get("body", "").strip()
                self.article_data_map[url] = {
                    "title": title,
                    "date": date.replace("\xa0", " "),
                    "body": body,
                    "url": [url]
                }
                articles.append(url)
        return articles

    def get_href(self, entry) -> str:
        return entry

    def get_title(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("title", "")

    def get_body(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("body", "")

    def get_images(self, response, entry=None) -> List[str]:
        return []

    def date_format(self) -> str:
        return '%Y-%m-%dT%H:%M:%S%z'

    def get_date(self, response) -> str:
        return self.article_data_map.get(response.request.meta.get('entry'), {}).get("date", "")

    def get_authors(self, response, entry=None) -> list[str]:
        return []

    def get_page_flag(self) -> bool:
        return False

    def get_next_page(self, response, current_page=None):
        payload = response.meta.get("payload", {})
        current_skip = int(payload.get("skip", 0))
        new_skip = current_skip + 20
        if new_skip >= 2160:
            return None
        return new_skip

    def go_to_next_page(self, response, start_url, current_page=None):
        api_url = response.meta.get("api_url")
        payload = response.meta.get("payload", {})
        if not api_url:
            return
        new_skip = self.get_next_page(response, current_page)
        if new_skip is not None:
            payload["skip"] = new_skip
            url = f"{self.api_start_url[start_url]['url']}&$skip={new_skip}"
            yield scrapy.Request(
                url=url,
                method='GET',
                callback=self.parse_intermediate,
                meta={
                    "start_url": start_url,
                    "api_url": url,
                    "payload": payload,
                },
                dont_filter=True 
            )
        else:
           return 