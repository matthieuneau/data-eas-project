import requests
from typing import List, Dict
import xml.etree.ElementTree as ET


# Function to fetch metadata from arXiv
def fetch_arxiv_metadata(query: str, max_results=5) -> List[Dict]:
    """
    Returns metadata of the articles from arXiv based on the search query.
    """
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,  # The search query, e.g., "all:deep learning"
        "start": 0,  # The index of the first result
        "max_results": max_results,  # Number of results to return
    }

    # Make the request to the arXiv API
    response = requests.get(base_url, params=params)
    # print(response.content)

    if response.status_code == 200:
        # Parse the XML response
        root = ET.fromstring(response.content)

        results = []

        # Extract metadata from each entry
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            title = entry.find("{http://www.w3.org/2005/Atom}title").text
            authors = [
                author.find("{http://www.w3.org/2005/Atom}name").text
                for author in entry.findall("{http://www.w3.org/2005/Atom}author")
            ]
            published = entry.find("{http://www.w3.org/2005/Atom}published").text
            summary = entry.find("{http://www.w3.org/2005/Atom}summary").text.strip()
            link_to_article = entry.find("{http://www.w3.org/2005/Atom}link").attrib[
                "href"
            ]

            results.append(
                {
                    "title": title,
                    "authors": authors,
                    "published": published,
                    "summary": summary,
                    "link": link_to_article,
                }
            )

    else:
        print(f"Error: Unable to fetch data (status code: {response.status_code})")

    return results


if __name__ == "__main__":
    query = "all:deep learning"  # Search query
    res = fetch_arxiv_metadata(query, max_results=3)  # Fetch 3 results
    print(res)
