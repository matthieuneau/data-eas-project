"""
This is a recursive crawler that starts from a given article and crawls all the papers it references, 
and repeats the process until a specified maximum depth.
"""

from processPdf import extract_text_from_pdf
from getReferencesArticles import extract_arxiv_references_from_article
from fetchArticleMetadata import fetch_arxiv_metadata
from saveToGraphDb import add_paper_to_db, add_relation_to_db


class RecursiveCrawler:
    def __init__(self, initial_id: str, max_depth: int):
        """
        Initializes the crawler with starting article ID, max depth, and a set of visited papers.
        """
        self.initial_id = initial_id  # Starting paper ID (e.g., "1805.08355")
        self.max_depth = max_depth  # Maximum depth for exploration
        self.visited_ids = set()  # Set to track visited articles

    def get_article_references(self, article_id: str) -> list:
        """
        Extracts references from the ArXiv PDF.
        """
        pdf_url = f"http://arxiv.org/pdf/{article_id}.pdf"
        print(f"Downloading PDF for {article_id}...")
        text = extract_text_from_pdf(pdf_url)
        references = extract_arxiv_references_from_article(text)
        print(f"Extracted references for {article_id}: {references}")
        return references
    
    def format_metadata_for_db(self, metadata: dict, article_id: str) -> dict:
        """
        Formats metadata to match the arguments required by `add_paper_to_db`.
        """
        title = metadata.get("title", "Unknown Title")
        authors = metadata.get("authors", [])
        publication_year = int(metadata.get("published", "0000").split("-")[0])  # Extract year from the date
        paper_index = article_id  # ArXiv ID is the paper index
        
        print(f"Formatted metadata for {article_id}: title={title}, authors={authors}, year={publication_year}, paper_index={paper_index}")
        
        return {
            "title": title,
            "authors": authors,
            "publication_year": publication_year,
            "paper_index": paper_index
        }

    def crawl_article(self, article_id: str, depth: int):
        """
        Recursively crawls an article, adding it to the graph and exploring its references.
        """
        if depth > self.max_depth:
            print(f"Reached maximum depth for {article_id}")
            return
    
        if article_id in self.visited_ids:
            print(f"Already visited {article_id}, skipping...")
            return

        # Mark the article as visited **before** any recursion
        self.visited_ids.add(article_id)
        
        print(f"Crawling article {article_id} at depth {depth}...")

        try:
            # Step 1: Get metadata for the paper
            metadata = fetch_arxiv_metadata(f"id:{article_id}")
            print(f"Fetched metadata for {article_id}: {metadata}")
        
            # Step 2: Format the metadata
            formatted_metadata = self.format_metadata_for_db(metadata, article_id)
            print(f"Formatted metadata: {formatted_metadata}")
        
            # Step 3: Add paper to database
            print(f"Saving paper to database: {formatted_metadata}")
            add_paper_to_db(
                title=formatted_metadata["title"],
                authors=formatted_metadata["authors"],
                paper_index=formatted_metadata["paper_index"],
                publication_year=formatted_metadata["publication_year"]
            )

            # Step 4: Get references from the PDF
            if depth < self.max_depth:  # Prevent recursive crawling beyond max_depth
                references = self.get_article_references(article_id)
                print(f"References for {article_id}: {references}")
            
                # Step 5: Add relationships and recursively crawl references
                for ref_id in references:
                    print(f"Adding relationship: {article_id} -> {ref_id}")
                    add_relation_to_db(article_id, ref_id)
                    self.crawl_article(ref_id, depth + 1)
                    
        except Exception as e:
            print(f"Error processing {article_id}: {e}")


if __name__ == "__main__":
    crawler = RecursiveCrawler(initial_id="1805.08355", max_depth=1)
    crawler.crawl_article(crawler.initial_id, 0)