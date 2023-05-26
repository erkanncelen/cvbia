from pdf2embeddings.scraper import DocumentScraper
from pdf2embeddings.arrange_text import CorpusGenerator


scraper = DocumentScraper(pdfs_folder, json_path)
df_by_page = scraper.document_corpus_to_pandas_df()