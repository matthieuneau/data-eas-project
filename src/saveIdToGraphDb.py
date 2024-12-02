"""
This file contains functions that save paper ids and its references to a Neo4j graph database.
"""
from typing import List
from neo4j import GraphDatabase
from dotenv import load_dotenv
import os

load_dotenv()

NEO4J_URI = os.getenv("NEO4J_URI", "bolt://localhost:7687")
NEO4J_USER = os.getenv("NEO4J_USER", "neo4j")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD", "password")

print(NEO4J_USER)

driver = GraphDatabase.driver(
    NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD)    
)

def add_paper_to_db(
    paper_id: str, references: List[str]
) -> None:
    """
    Add a paper to the graph database.

    :param paper_id: The unique identifier of the paper.
    :param references: The arxiv ids that the paper references.
    """
    query = """
    MERGE (p:Paper {paper_index: $paper_index})
    SET p.references = $references
    """

    with driver.session() as session:
        session.execute_write(
            lambda tx: tx.run(
                query,
                paper_index=paper_id,
                references=references,
            )
        )

def count_papers() -> int:
    """
    Count the number of papers in the graph database.

    :return: The number of papers in the database.
    """
    query = """
    MATCH (p:Paper)
    RETURN count(p) as count
    """

    with driver.session() as session:
       return session.execute_read(
            lambda tx: tx.run(query).single()["count"]
        )
        

if __name__ == "__main__":
    print(count_papers())