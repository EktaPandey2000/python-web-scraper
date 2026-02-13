import scrapy
import json
from scraper.OCSpider import OCSpider
from bs4 import BeautifulSoup

class GovernorOfWyoming(OCSpider):
    name = 'GovernorOfWyoming'
    language = 'English'
    country = 'US'

    start_urls_names = {
        'https://governor.wyo.gov/news-releases':''
    }

    def parse_intermediate(self, response):

        if not response.request.body:
            payload = {
                "operationName": "PressReleaseSearch",
                "variables": {
                    "parameters": "{\"fulltext\":\"\",\"year\":\"\",\"size\":\"10\",\"from\":\"0\"}"
                },
                "query": """
                query PressReleaseSearch($parameters: String!) {
                  pressReleaseSearch(parameters: $parameters) {
                    items {
                      ...PressRelease
                      __typename
                    }
                    total
                    __typename
                  }
                }

                fragment PressRelease on PressRelease {
                  path
                  displayText
                  releaseDate
                  htmlContent {
                    content {
                      html
                      __typename
                    }
                    __typename
                  }
                  image {
                    urls
                    __typename
                  }
                  __typename
                }
                """
            }
            form_data = json.dumps(payload)
        else:
            form_data = response.request.body

        headers = {"Content-Type": "application/json"}
        request = scrapy.Request(
            url='https://governor.wyo.gov/api/cms/graphql',
            method="POST",
            body=form_data,
            headers=headers,
            callback=self.parse,
            dont_filter=True
        )
        request.meta["start_url"] = response.request.meta.get("start_url", response.url)
        yield request

    def get_page_flag(self) -> bool:
        return False

    @property
    def source_type(self) -> str:
        return 'ministry'

    @property
    def timezone(self):
        return "America/Denver"

    def get_articles(self, response) -> list:
        try:
            data = json.loads(response.text)
        except json.JSONDecodeError:
            return []
        records = data.get("data", {}).get("pressReleaseSearch", {}).get("items", [])
        base_url = response.request.meta.get("start_url", "")
        self.articles_data = []
        self.articles_info = {}
        for article in records:
            path = article.get("path", "")
            full_url = f"{base_url}/{path}" if path else base_url
            article_data = {
                "displayText": article.get("displayText", ""),
                "releaseDate": article.get("releaseDate", ""),
                "htmlContent": article.get("htmlContent", {}).get("content", {}).get("html", "")
            }
            self.articles_info[full_url] = article_data
            self.articles_data.append(full_url)
        return self.articles_data

    def get_href(self, entry) -> str:
        return entry if isinstance(entry, str) else ""

    def get_title(self, response) -> str:
        return self.articles_info.get(response.url, {}).get("displayText", "").strip()

    def get_body(self, response) -> str:
        html_content = self.articles_info.get(response.url, {}).get("htmlContent", "")
        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            return soup.get_text(separator=" ", strip=True)
        return ""

    def date_format(self) -> str:
        return '%Y-%m-%d'

    def get_date(self, response) -> str:
        return self.articles_info.get(response.url, {}).get("releaseDate", "").strip()

    def get_images(self, response) -> list:
        html_content = self.articles_info.get(response.url, {}).get("htmlContent", "")
        if html_content:
            soup = BeautifulSoup(html_content, "html.parser")
            return [response.urljoin(img["src"]) for img in soup.find_all("img") if "src" in img]
        return []

    def get_authors(self, response):
        return []

    def go_to_next_page(self, response, start_url, current_page = None):
        form_data = response.request.body
        try:
            form_data_dict = json.loads(form_data) if isinstance(form_data, bytes) else json.loads(
                form_data.decode('utf-8'))
            variables = form_data_dict.get("variables", {})
            parameters_str = variables.get("parameters", "{}")
            parameters = json.loads(parameters_str)
            parameters["from"] = str(int(parameters.get("from", "0")) + 10)
            variables["parameters"] = json.dumps(parameters)
            form_data_dict["variables"] = variables
            updated_form_data = json.dumps(form_data_dict)
        except json.JSONDecodeError:
            return  None
        request = response.request.replace(
                url = response.url,
                body = updated_form_data,
                callback = self.parse_intermediate
        )
        request.meta["start_url"] = start_url
        yield request