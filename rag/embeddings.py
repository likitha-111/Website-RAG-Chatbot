from sentence_transformers import SentenceTransformer
import os

from dotenv import load_dotenv

load_dotenv()

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)