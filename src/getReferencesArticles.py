import re


# TODO: Improve the function to return other references than ArXiv references
def extract_references_from_article(text: str) -> list:
    """
    Extract all the ArXiv references from the text of an article.
    :param text: The text of the article.
    :return: A list of ArXiv urls to pdfs
    """
    references = re.findall(r"arXiv:\d{4}\.\d{4,5}", text)
    return references


if __name__ == "__main__":
    from process_pdf import extract_text_from_pdf

    text = extract_text_from_pdf("http://arxiv.org/pdf/1805.08355v1")
    references = extract_references_from_article(text)
    print(references)
