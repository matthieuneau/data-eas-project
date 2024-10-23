CREATE TABLE articles (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255),
    authors VARCHAR(255),
    year INT,
    arxiv_id VARCHAR(20),
    pdf_url TEXT
);

