from __future__ import annotations
from abc import ABC, abstractmethod
from pathlib import Path

from docx import Document as DocxDocument
from pdfminer.high_level import extract_text as extract_pdf_text


class DocumentLoader(ABC):
    @abstractmethod
    def load(self, path: str) -> str:
        raise NotImplementedError


class DocxDocumentLoader(DocumentLoader):
    def load(self, path: str) -> str:
        document = DocxDocument(path)
        paragraphs = [paragraph.text for paragraph in document.paragraphs if paragraph.text.strip()]
        return "\n".join(paragraphs)


class PdfDocumentLoader(DocumentLoader):
    def load(self, path: str) -> str:
        return extract_pdf_text(path) or ""


class DocumentLoaderFactory:
    SUPPORTED_LOADERS = {
        ".docx": DocxDocumentLoader,
        ".pdf": PdfDocumentLoader,
    }

    @classmethod
    def get_loader(cls, path: str) -> DocumentLoader:
        extension = Path(path).suffix.lower()
        loader_class = cls.SUPPORTED_LOADERS.get(extension)
        if loader_class is None:
            raise ValueError(f"Unsupported document type: {extension}")
        return loader_class()
