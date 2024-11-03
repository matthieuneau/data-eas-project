from typing import List
from neo4j import GraphDatabase

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "Arxiv123"))


def add_paper_to_db(
    title: str, authors: List[str], paper_index: str, publication_year: int
) -> None:
    """
    Add a paper to the graph database.
    """
    # TODO: move to .env
    query = """
    MERGE (p:Paper {paper_index: $paper_index})
    SET p.title = $title,
        p.authors = $authors,
        p.publication_year = $publication_year
    """

    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run(
                query,
                title=title,
                paper_index=paper_index,
                authors=authors,
                publication_year=publication_year,
            )
        )


if __name__ == "__main__":
    add_paper_to_db(
        title="A new paper",
        paper_index="1234.56789",
        authors=["John Doe", "Jane Doe"],
        publication_year=2021,
    )


def add_relation_to_db(paper_index1: str, paper_index2: str) -> None:
    """
    Add a citation relation between two papers in the graph database.

    :param paper_index1: The unique identifier (e.g., DOI) of the citing paper.
    :param paper_index2: The unique identifier of the cited paper.
    """
    query = """
    MATCH (p1:Paper {paper_index: $paper_index1})
    MATCH (p2:Paper {paper_index: $paper_index2})
    MERGE (p1)-[:CITES]->(p2)
    """

    with driver.session() as session:
        session.write_transaction(
            lambda tx: tx.run(
                query, paper_index1=paper_index1, paper_index2=paper_index2
            )
        )


if __name__ == "__main__":
    add_paper_to_db(
        title="A new paper",
        paper_index="1234.56789",
        authors=["John Doe", "Jane Doe"],
        publication_year=2021,
    )
    add_paper_to_db(
        title="Another paper",
        paper_index="9876.54321",
        authors=["Alice Smith", "Bob Smith"],
        publication_year=2020,
    )
    add_relation_to_db("1234.56789", "9876.54321")

# commit line 1
# commit line 2
# commit line 3
