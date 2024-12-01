"""
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

def get_method_id_for_api(method_name: str) -> int|None:
    """
    Retrieve the id of a method from the PapersWithCode API
    :param method_name: the name of the method
    :return: The id of the method
    """
    html = requests.get(f"https://paperswithcode.com/method/{method_name}")
    soup = BeautifulSoup(html.text, 'html.parser')
    
    # Extract the script tag content
    script_tags = soup.find_all('script')
    method_id = None

    for script in script_tags:
        if script.string and "DATATABLE_PAPERS_FILTER_VALUE" in script.string:
            # Extract the method_id using regex
            match = re.search(r"DATATABLE_PAPERS_FILTER_VALUE\s*=\s*'(\d+)'", script.string)
            if match:
                method_id = match.group(1)
                break

    if not method_id:
        print("Method ID not found in the HTML.")
    
    print(f"Extracted Method ID: {method_id}")

    return int(method_id) if method_id else None
