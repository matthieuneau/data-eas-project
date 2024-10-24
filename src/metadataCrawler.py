from processPdf import extract_text_from_pdf
from getReferencesArticles import extract_arxiv_references_from_article
from fetchArticleMetadata import fetch_arxiv_metadata
from saveMetadataToDb import store_articles_in_db
from typing import List


class MetadataCrawler:
    def __init__(self, initial_id: int, db: dict):
        self.db = db  # TODO: Move the connection info here
        self.scraped_counter = 0
        self.initial_id = initial_id
        self.visited_ids: List[int] = (
            []
        )  # List of ids of articles that have already been scraped
        self.queue = [self.initial_id]  # List of article ids to be scraped

    def get_article_arxiv_references(self, article_id: int):
        """
        Given an article id, reads the pdf and returns the references
        """
        pdf_url = f"http://arxiv.org/pdf/{article_id}"
        text = extract_text_from_pdf(pdf_url)
        references = extract_arxiv_references_from_article(text)
        return references

    # TODO: Check that the queue does not empty too often. Experiment to figure it out
    def __call__(self, max_articles: int = 10):
        while self.scraped_counter < max_articles and self.queue:
            current_id = self.queue.pop(0)
            references = self.get_article_arxiv_references(current_id)
            # TODO: Filter out articles that are already in the database??
            # Filter out already visited articles
            references = [
                reference
                for reference in references
                if reference not in self.visited_ids
            ]

            metadata = fetch_arxiv_metadata(f"id:{current_id}")
            store_articles_in_db(metadata)
            self.visited_ids.append(current_id)
            self.scraped_counter += 1
            self.queue.extend(references)


if __name__ == "__main__":
    crawler = MetadataCrawler("1805.08355", db={})
    crawler(max_articles=3)
