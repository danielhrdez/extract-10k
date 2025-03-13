import logging
import json
import re
from typing import Dict, List
from docling.document_converter import DocumentConverter
from langchain_openai import ChatOpenAI
from tqdm import tqdm
from bs4 import BeautifulSoup
from pypdf import PdfReader


class DocumentProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.debug("Initializing DocumentProcessor")
        self.doc_converter = DocumentConverter()
        self.llm = ChatOpenAI(model="o3-mini")
        self.logger.debug("DocumentProcessor initialized successfully")

    def download_and_convert_document(self, url: str) -> str:
        self.logger.debug(f"Attempting to download and convert document from: {url}")
        try:
            with tqdm(total=3, desc="Converting document") as pbar:
                if url.endswith(".html"):
                    with open(url, "r") as f:
                        content = f.read()
                    soup = BeautifulSoup(content, "html.parser")
                    content = soup.get_text()
                elif url.endswith(".pdf"):
                    reader = PdfReader(url)
                    content = ""
                    for page in reader.pages:
                        content += page.extract_text()
                else:
                    result = self.doc_converter.convert(url)
                    content = result.document.export_to_markdown()
                pbar.update(1)
            self.logger.info("Successfully converted document.")
            return content
        except Exception as e:
            self.logger.error(f"Error downloading/converting document: {str(e)}")
            raise

    def extract_target_section(self, document: str, target: str) -> str:
        self.logger.debug(f"Extracting target section: {target}")
        try:
            extracted = self.llm.invoke(
                f"Extract the section: {target} from the following document: {document}"
            )
            self.logger.info("Successfully extracted target section")
            return extracted.content

        except Exception as e:
            self.logger.error(f"Error extracting target section: {str(e)}")
            raise
