import argparse

from bs4 import BeautifulSoup

from utils import result_output


class ServiceSnippet:
    def __init__(self):
        self._key_snippets_map = dict()
        self.html = None

    def scrape_html(self, html: str):
        # using Snippet class to manage html str
        snippet = Snippet(html)

        for key in snippet.keys:

            if key not in self._key_snippets_map:
                self._key_snippets_map[key] = set()
            # store keys that exists in snippet (html)
            self._key_snippets_map[key].add(snippet)

        self.html = html

    def handle_request(self, request: dict) -> dict:

        intersected = None
        request_key = set()

        for element in request['selected_tags']:
            # snippets_set get a key if have match in html
            snippets_set = self._key_snippets_map.get(element['name'], set())
            # request_key get keys from selected tags
            request_key.add(element['name'])

            if not intersected:
                # if there is no intersected will ket the values for selected tags
                intersected = request_key

            else:

                intersected = request_key.intersection(snippets_set)

        return result_output(self, intersected, request, request_key)


# Class Snippet is helper to handle keys
class Snippet:
    def __init__(self, article):
        self._article = article
        soup = BeautifulSoup(article, 'html.parser')
        article_link = soup.find_all('article')
        tags = []
        if article_link:
            for article1 in article_link:
                val = article1.get('data-tags')
                val = frozenset(val.split(','))
                tags += val
        self._keys = set(tags)

    @property
    def article(self):
        return self._article

    @property
    def keys(self):
        return self._keys


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--html_path",
        help="path leading to the html file",
        type=str,
        required=True,
    )
    args = parser.parse_args()
    with open(args.html_path, "r") as f:
        html_str = f.read()
    service_funnel = ServiceSnippet()
    service_funnel.scrape_html(html_str)
