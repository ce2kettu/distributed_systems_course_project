# Sources:
# https://www.mediawiki.org/wiki/API:Links
# https://www.digitalocean.com/community/tutorials/how-to-use-threadpoolexecutor-in-python-3
# Could have also used a Wikipedia library like https://pypi.org/project/wikipedia/

import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_WIKI_URL = "https://en.wikipedia.org/wiki/"


def is_page_valid(pageTitle):
    try:
        res = requests.get(url=WIKIPEDIA_WIKI_URL + pageTitle)
        return res.status_code == 200
    except:
        return False


def get_page_links(pageTitle):
    links = []

    query_params = {
        "action": "query",
        "format": "json",
        "titles": pageTitle,
        "prop": "links",
        "pllimit": 500,
    }

    # initial API request to fetch article links
    data = wikipedia_query(query_params)
    pages = data["query"]["pages"]
    insert_links_to_list(pages, links)

    # API indicates that there are more links than 'pllimit'
    while "continue" in data:
        # continue from last query
        query_params["plcontinue"] = data["continue"]["plcontinue"]
        data = wikipedia_query(query_params)
        pages = data["query"]["pages"]
        insert_links_to_list(pages, links)

    return links


def wikipedia_query(params):
    res = requests.get(url=WIKIPEDIA_API_URL, params=params)
    return res.json()


def insert_links_to_list(pages, list):
    for k, v in pages.items():
        for link in v["links"]:
            list.append(link["title"])
