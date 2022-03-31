# Sources:
#
# Wikipedia API:
# https://www.mediawiki.org/wiki/API:Links
# https://github.com/martin-majlis/Wikipedia-API/blob/master/wikipediaapi/__init__.py
# Could have also used a Wikipedia library like https://pypi.org/project/wikipedia/

import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_WIKI_URL = "https://en.wikipedia.org/wiki/"


def is_page_valid(page_title):
    try:
        if len(page_title.strip()) == 0:
            return False

        res = requests.get(url=WIKIPEDIA_WIKI_URL + page_title)
        return res.status_code == 200
    except Exception as e:
        print(f"Failed to check page '{page_title}' validity: {e}")
        return False


def get_page_links(page_title):
    try:
        links = []
        query_params = {
            "action": "query",
            "format": "json",
            "titles": page_title,
            "prop": "links",
            "pllimit": 500,
        }

        # initial API request to fetch article links
        data = wikipedia_query(query_params)
        pages = data["query"]["pages"]
        append_link_titles_to_list(pages, links)

        # the API indicates that there are more links than 'pllimit'
        while "continue" in data:
            # continue from the last query
            query_params["plcontinue"] = data["continue"]["plcontinue"]
            data = wikipedia_query(query_params)
            pages = data["query"]["pages"]
            append_link_titles_to_list(pages, links)

        return (links, page_title)
    except Exception as e:
        print(f"Failed to get page links '{page_title}': {e}")
        return ([], page_title)

def wikipedia_query(params):
    res = requests.get(url=WIKIPEDIA_API_URL, params=params)
    return res.json()


def append_link_titles_to_list(pages, list):
    for _, v in pages.items():
        if "links" in v:
            for link in v["links"]:
                list.append(link["title"])
