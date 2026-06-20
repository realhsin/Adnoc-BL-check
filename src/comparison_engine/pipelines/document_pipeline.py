from __future__ import annotations
from typing import Dict, Optional

from comparison_engine.adapters.document_loader import DocumentLoaderFactory
from comparison_engine.domain.models.shipment import Shipment
from comparison_engine.services.suggestion_service import SuggestionService
from comparison_engine.transformers.ai_extractor import AIExtractionProvider
from comparison_engine.transformers.normalizer import FieldNormalizer
from comparison_engine.use_cases.compare_shipments import CompareShipments, ComparisonResult


class DocumentPipeline:
    @classmethod
    def load_document_text(cls, path: str) -> str:
        loader = DocumentLoaderFactory.get_loader(path)
        return loader.load(path)

    @classmethod
    def extract_shipment(cls, raw_text: str) -> Shipment:
        extracted = AIExtractionProvider.extract_fields(raw_text, Shipment.FIELDS)
        normalized = FieldNormalizer.normalize(extracted)
        return Shipment(**normalized)

    @classmethod
    def compare_document_pair(cls, left_path: str, right_path: str) -> Dict[str, Optional[str | list | dict]]:
        left_text = cls.load_document_text(left_path)
        right_text = cls.load_document_text(right_path)

        left_extracted = AIExtractionProvider.extract_fields(left_text, Shipment.FIELDS)
        right_extracted = AIExtractionProvider.extract_fields(right_text, Shipment.FIELDS)
        left_normalized = FieldNormalizer.normalize(left_extracted)
        right_normalized = FieldNormalizer.normalize(right_extracted)

        left_shipment = Shipment(**left_normalized)
        right_shipment = Shipment(**right_normalized)
        comparison_result: ComparisonResult = CompareShipments.compare(left_shipment, right_shipment)

        return {
            "left_shipment": left_shipment,
            "right_shipment": right_shipment,
            "report": comparison_result,
            "left_suggestions": SuggestionService.build_suggestions(left_extracted),
            "right_suggestions": SuggestionService.build_suggestions(right_extracted),
        }
