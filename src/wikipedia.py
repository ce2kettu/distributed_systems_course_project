# Sources:
#
# Wikipedia API:
# https://www.mediawiki.org/wiki/API:Links
# https://github.com/martin-majlis/Wikipedia-API/blob/master/wikipediaapi/__init__.py
# Could have also used a Wikipedia library like https://pypi.org/project/wikipedia/

import requests

WIKIPEDIA_API_URL = "https://en.wikipedia.org/w/api.php"
WIKIPEDIA_WIKI_URL = "https://en.wikipedia.org/wiki/"


def is_page_valid(pageTitle):
    try:
        if len(pageTitle.strip()) == 0:
            return False

        res = requests.get(url=WIKIPEDIA_WIKI_URL + pageTitle)
        return res.status_code == 200
    except Exception as e:
        print(f"Failed to check page '{pageTitle}' validity: {e}")
        return False


def get_page_links(pageTitle):
    try:
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
        append_link_titles_to_list(pages, links)

        # the API indicates that there are more links than 'pllimit'
        while "continue" in data:
            # continue from the last query
            query_params["plcontinue"] = data["continue"]["plcontinue"]
            data = wikipedia_query(query_params)
            pages = data["query"]["pages"]
            append_link_titles_to_list(pages, links)

        return (links, pageTitle)
    except Exception as e:
        print(f"Failed to get page links '{pageTitle}': {e}")
        return ([], pageTitle)

def wikipedia_query(params):
    res = requests.get(url=WIKIPEDIA_API_URL, params=params)
    return res.json()


def append_link_titles_to_list(pages, list):
    for _, v in pages.items():
        if "links" in v:
            for link in v["links"]:
                list.append(link["title"])
