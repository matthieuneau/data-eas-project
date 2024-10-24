import psycopg2
from typing import List, Dict


def store_articles_in_db(articles: List[Dict]) -> None:
    conn = psycopg2.connect(
        dbname="postgres",
        user="matthieuneau",
        password="postgres",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()

    # Prepare the insert statement
    insert_query = """
        INSERT INTO articles (title, authors, year, arxiv_id, pdf_url)
        VALUES (%s, %s, %s, %s, %s)
    """

    for article in articles:
        title = article.get("title", "")[:255]  # Limit title to 255 characters
        authors = ", ".join(article.get("authors", []))
        year = (
            int(article["publication_date"][:4])
            if "publication_date" in article
            else None
        )
        arxiv_id = article["link"].split("/")[-1]
        pdf_url = article["link"].replace("abs", "pdf")

        # Insert the article into the database
        cursor.execute(insert_query, (title, authors, year, arxiv_id, pdf_url))

    # Commit the transaction
    conn.commit()

    # Close the cursor and connection
    cursor.close()
    conn.close()


if __name__ == "__main__":
    articles = [
        {
            "title": "Opening the black box of deep learning",
            "authors": ["Dian Lei", "Xiaoxiao Chen", "Jianfei Zhao"],
            "published": "2018-05-22T02:12:33Z",
            "summary": "The great success of deep learning shows that its technology contains\nprofound truth, and understanding its internal mechanism not only has important\nimplications for the development of its technology and effective application in\nvarious fields, but also provides meaningful insights into the understanding of\nhuman brain mechanism. At present, most of the theoretical research on deep\nlearning is based on mathematics. This dissertation proposes that the neural\nnetwork of deep learning is a physical system, examines deep learning from\nthree different perspectives: microscopic, macroscopic, and physical world\nviews, answers multiple theoretical puzzles in deep learning by using physics\nprinciples. For example, from the perspective of quantum mechanics and\nstatistical physics, this dissertation presents the calculation methods for\nconvolution calculation, pooling, normalization, and Restricted Boltzmann\nMachine, as well as the selection of cost functions, explains why deep learning\nmust be deep, what characteristics are learned in deep learning, why\nConvolutional Neural Networks do not have to be trained layer by layer, and the\nlimitations of deep learning, etc., and proposes the theoretical direction and\nbasis for the further development of deep learning now and in the future. The\nbrilliance of physics flashes in deep learning, we try to establish the deep\nlearning technology based on the scientific theory of physics.",
            "link": "http://arxiv.org/abs/1805.08355v1",
        }
    ]
    store_articles_in_db(articles)
