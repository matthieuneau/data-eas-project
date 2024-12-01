This file contains functions that retrieve all the arXiv papers corresponding to a given method from the PapersWithCode website
"""

from typing import Set
import requests
import re
from bs4 import BeautifulSoup 


def retrieve_arxiv_id(paper_url: str) -> str|None:
    """
    Retrieve the arXiv id of a given paper from the PapersWithCode website. Returns None if the paper is not on arXiv.
    :param paper_url: the url of the paper on the PapersWithCode website
    :return: The id of the arXiv paper corresponding to the method
    """
    html = requests.get(paper_url)
    arxiv_id = re.findall(r"https:\/\/arxiv\.org\/pdf\/[a-zA-Z0-9\-]+(?:\.[a-zA-Z0-9\-]+)*\.pdf", html.text)
    return arxiv_id[0].split("/")[-1].strip(".pdf") if arxiv_id else None
