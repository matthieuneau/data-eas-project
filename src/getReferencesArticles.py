"""
Helper function to extract the ArXiv references codes from an article 
"""

import re
from typing import List


# TODO: Improve the function to return other references than ArXiv references
def extract_arxiv_references_from_article(text: str) -> List[str]:
    """
    returns a list of ids corresponding the t
    """
    references = re.findall(r"arXiv:\d{4}\.\d{4,5}", text)
    references = [reference.split(":")[1] for reference in references]
    return references


if __name__ == "__main__":
    from processPdf import extract_text_from_pdf

    text = extract_text_from_pdf("http://arxiv.org/pdf/1805.08355v1")
    references = extract_arxiv_references_from_article(text)
    print(references)
