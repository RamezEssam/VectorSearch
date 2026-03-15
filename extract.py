import fitz  # PyMuPDF
import re
import os

# -----------------------------
# CONFIG
# -----------------------------
pdf_path = "law.pdf"
output_folder = "extracted_articles"
article_marker = "Article" 

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def split_arabic_english(text):
    """Separates Arabic and English text based on Unicode ranges."""
    arabic = ''.join(re.findall(r'[\u0600-\u06FF\s]+', text))
    english = ''.join(re.findall(r'[A-Za-z0-9\s\.,;:!?\'"()-]+', text))
    return arabic.strip(), english.strip()

def extract_articles_from_page(text):
    """Splits a page into articles based on a marker."""
    parts = text.split(article_marker)
    articles = []
    for part in parts:
        articles.append(article_marker + part.strip())
    return articles

# -----------------------------
# PROCESS PDF
# -----------------------------
doc = fitz.open(pdf_path)
all_articles = []

for page_num, page in enumerate(doc, start=1):
    page_text = page.get_text("text")
    articles_on_page = extract_articles_from_page(page_text)
    all_articles.extend(articles_on_page)

# -----------------------------
# SAVE ARTICLES
# -----------------------------
for idx, article in enumerate(all_articles, start=1):
    ar_text, en_text = split_arabic_english(article)

    ar_file = os.path.join(output_folder, f"article_{idx}_ar.txt")
    en_file = os.path.join(output_folder, f"article_{idx}_en.txt")

    with open(ar_file, "w", encoding="utf-8") as f:
        f.write(ar_text)

    with open(en_file, "w", encoding="utf-8") as f:
        f.write(en_text)

print(f"Done! Extracted {len(all_articles)} articles to '{output_folder}' folder.")