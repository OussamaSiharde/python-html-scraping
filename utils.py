from bs4 import BeautifulSoup

"""
    result_output is a function that will handle returning article and tags 

"""


def result_output(self, intersected, request: dict, request_key: set) -> dict:
    result = dict()

    tag_count_in_req = len(request['selected_tags'])
    # intersected will get 0 if the selected tags has no match in any article
    if not intersected:
        msg = {"code": 2, "msg": "Invalid tags"}
        result['snippet'] = None
        result['next_tags'] = []
        result['status'] = msg
        result['selected_tags'] = request['selected_tags']
        return result
    # intersected will get 1 if the selected tag is valid but there is no article related to it
    elif len(intersected) == 1:
        msg = {"code": 1, "msg": "Valid tags but no snippet"}
        result['status'] = msg
        result['snippet'] = None
        result['selected_tags'] = request['selected_tags']
        result['next_tags'] = get_tags(self.html, intersected)
        return result
    # intersected will get more 1 if the selected tag is valid but there is article related to it
    else:
        msg = {"code": 0, "msg": "Valid tags with snippet"}
        snippet = set(intersected)
        result['snippet'] = get_article(self.html, snippet)
        result['status'] = msg
        result['selected_tags'] = request['selected_tags']

        if len(snippet) == tag_count_in_req:
            result['next_tags'] = []
            return result

        else:
            missing_keys = request_key.symmetric_difference(set(intersected))
            result['next_tags'] = list(missing_keys)
        return result


"""
    get article is a helper function that take html as string and 
    keys and returns the related article 

"""


def get_article(article, keys: set):
    soup = BeautifulSoup(article, 'html.parser')
    article_link = soup.find_all('article')
    if article_link:
        for article1 in article_link:
            val = article1.get('data-tags')
            val = frozenset(val.split(','))

            if all(elem in list(keys) for elem in list(val)):
                return str(article1)


"""
    get tags is a helper function that take html as string and 
    keys and returns tags excluding keys values
    
"""


def get_tags(article, keys: set):
    soup = BeautifulSoup(article, 'html.parser')
    article_link = soup.find_all('article')
    tags = []
    if article_link:
        for article1 in article_link:
            val = article1.get('data-tags')
            val = frozenset(val.split(','))
            tags += val

    return [{"name": tag} for tag in sorted(set(tags).symmetric_difference(keys), key=str)]
