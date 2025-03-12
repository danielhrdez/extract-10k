import logging
from typing import Dict, List
from docling.document_converter import DocumentConverter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from tqdm import tqdm


class DocumentProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing DocumentProcessor")
        self.doc_converter = DocumentConverter()
        self.embeddings = HuggingFaceEmbeddings()
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        self.logger.debug("DocumentProcessor initialized successfully")

    def download_and_convert_document(self, url: str) -> Dict:
        self.logger.debug(f"Attempting to download and convert document from: {url}")
        try:
            with tqdm(total=3, desc="Converting document") as pbar:
                result = self.doc_converter.convert(url)
                pbar.update(1)

                content = result.document.export_to_markdown()
                pbar.update(1)

            self.logger.info("Successfully converted document.")
            return {
                "content": content,
                "raw": result.document.export_to_dict(),
            }
        except Exception as e:
            self.logger.error(f"Error downloading/converting document: {str(e)}")
            raise

    def create_chunks(self, document_data: Dict) -> List[str]:
        self.logger.debug("Starting document chunking process")
        try:
            with tqdm(total=3, desc="Creating chunks") as pbar:
                text_splitter = RecursiveCharacterTextSplitter(
                    chunk_size=8192,
                    chunk_overlap=1024,
                    separators=["\n\n", "\n", ".", "!", "?", ",", " ", ""],
                )
                pbar.update(1)

                content = document_data["content"]
                combined_text = content
                pbar.update(1)

                chunks = text_splitter.split_text(combined_text)
                pbar.update(1)

            self.logger.info(f"Created {len(chunks)} chunks from document")
            return chunks
        except Exception as e:
            self.logger.error(f"Error creating chunks: {str(e)}")
            raise

    def create_vector_store(self, chunks: List[str]) -> FAISS:
        self.logger.debug("Creating vector store")
        try:
            with tqdm(total=1, desc="Creating vector store") as pbar:
                vector_store = FAISS.from_texts(chunks, self.embeddings)
                pbar.update(1)

            self.logger.info("Vector store created successfully")
            return vector_store
        except Exception as e:
            self.logger.error(f"Error creating vector store: {str(e)}")
            raise

    def find_relevant_sections(self, vector_store: FAISS, query: str) -> List[str]:
        self.logger.debug(f"Searching for sections relevant to: {query}")
        try:
            with tqdm(total=2, desc="Finding relevant sections") as pbar:
                results = vector_store.similarity_search(query, k=10)
                pbar.update(1)

                relevant_texts = [doc.page_content for doc in results]
                pbar.update(1)

            self.logger.info(f"Found {len(relevant_texts)} relevant sections")
            return relevant_texts
        except Exception as e:
            self.logger.error(f"Error finding relevant sections: {str(e)}")
            raise

    def extract_target_section(self, relevant_sections: List[str], target: str) -> str:
        self.logger.debug(f"Extracting target section: {target}")
        try:
            with tqdm(total=2, desc="Extracting target section") as pbar:
                combined_text = "\n\n".join(relevant_sections)
                print(combined_text)
                prompt = f"Extract the {target} section from the following text:\n\n{combined_text}"
                pbar.update(1)

                response = self.llm.invoke(prompt)
                print(response)
                pbar.update(1)

            self.logger.info("Successfully extracted target section")
            return response
        except Exception as e:
            self.logger.error(f"Error extracting target section: {str(e)}")
            raise
