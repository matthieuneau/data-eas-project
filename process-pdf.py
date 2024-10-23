import requests
import pdfplumber


def extract_text_from_pdf(url):
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to download the PDF: {response.status_code}")

    # Write the PDF content to a local file
    pdf_path = "downloaded_paper.pdf"
    with open(pdf_path, "wb") as f:
        f.write(response.content)

    # Extract text from the PDF
    with pdfplumber.open(pdf_path) as pdf:
        all_text = ""
        for page in pdf.pages:
            all_text += page.extract_text() + "\n"

    return all_text


# Example usage
url = "http://arxiv.org/pdf/1805.08355v1"
text = extract_text_from_pdf(url)
print(text[:1000])  # Print the first 1000 characters of the extracted text
