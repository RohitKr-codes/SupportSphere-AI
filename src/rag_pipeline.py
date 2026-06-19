from pathlib import Path
from pypdf import PdfReader

import chromadb
from sentence_transformers import SentenceTransformer

from src.config import Config


class RAGPipeline:

    def __init__(self):

        self.embedding_model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

        self.client = chromadb.PersistentClient(
            path=Config.CHROMA_DB_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name="support_kb"
        )

    # ----------------------------
    # PDF Loader
    # ----------------------------

    def load_pdf(self, filepath):

        documents = []

        pdf = PdfReader(filepath)

        for page_num, page in enumerate(pdf.pages):

            text = page.extract_text()

            if text:

                documents.append({
                    "text": text,
                    "source": Path(filepath).name,
                    "page": page_num + 1
                })

        return documents

    # ----------------------------
    # TXT Loader
    # ----------------------------

    def load_txt(self, filepath):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        return [{
            "text": text,
            "source": Path(filepath).name,
            "page": 1
        }]

    # ----------------------------
    # Markdown Loader
    # ----------------------------

    def load_md(self, filepath):

        with open(
            filepath,
            "r",
            encoding="utf-8"
        ) as f:

            text = f.read()

        return [{
            "text": text,
            "source": Path(filepath).name,
            "page": 1
        }]

    # ----------------------------
    # Chunking
    # ----------------------------

    def chunk_text(
        self,
        text,
        chunk_size=500,
        overlap=100
    ):

        chunks = []

        start = 0

        while start < len(text):

            end = start + chunk_size

            chunk = text[start:end]

            chunks.append(chunk)

            start += (
                chunk_size - overlap
            )

        return chunks

    # ----------------------------
    # Document Processing
    # ----------------------------

    def process_documents(self):

        data_folder = Path("data")

        all_chunks = []

        for file in data_folder.iterdir():

            documents = []

            if file.suffix.lower() == ".pdf":

                documents = self.load_pdf(file)

            elif file.suffix.lower() == ".txt":

                documents = self.load_txt(file)

            elif file.suffix.lower() == ".md":

                documents = self.load_md(file)

            for doc in documents:

                chunks = self.chunk_text(
                    doc["text"]
                )

                for chunk in chunks:

                    all_chunks.append({
                        "text": chunk,
                        "source": doc["source"],
                        "page": doc["page"]
                    })

        return all_chunks

    # ----------------------------
    # Vector Index Creation
    # ----------------------------

    def build_index(self):

        chunks = self.process_documents()

        if not chunks:

            print("No documents found.")
            return

        texts = [
            chunk["text"]
            for chunk in chunks
        ]

        embeddings = self.embedding_model.encode(
            texts
        ).tolist()

        ids = [
            f"doc_{i}"
            for i in range(
                len(chunks)
            )
        ]

        metadatas = []

        for chunk in chunks:

            metadatas.append({
                "source": chunk["source"],
                "page": chunk["page"]
            })

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas
        )

        print(
            f"Indexed {len(chunks)} chunks"
        )

    # ----------------------------
    # Retrieval
    # ----------------------------

    def retrieve(
        self,
        query,
        top_k=5
    ):

        query_embedding = (
            self.embedding_model.encode(
                query
            ).tolist()
        )

        results = self.collection.query(
            query_embeddings=[
                query_embedding
            ],
            n_results=top_k
        )

        retrieved_docs = []

        documents = results["documents"][0]

        metadatas = results["metadatas"][0]

        distances = results["distances"][0]

        for doc, meta, dist in zip(
            documents,
            metadatas,
            distances
        ):

            confidence = round(
                1 / (1 + dist),
                2
            )

            retrieved_docs.append({

                "content": doc,

                "source":
                meta["source"],

                "page":
                meta["page"],

                "confidence":
                confidence
            })

        return retrieved_docs