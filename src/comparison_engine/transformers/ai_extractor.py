from __future__ import annotations
import json
import os
from typing import Dict, Optional, Sequence

from comparison_engine.transformers.field_extractor import FieldExtractor

try:
    import openai
except ImportError:  # pragma: no cover
    openai = None


class AIExtractionProvider:
    MODEL = "gpt-3.5-turbo"

    @classmethod
    def service_available(cls) -> bool:
        return openai is not None and bool(os.getenv("OPENAI_API_KEY"))

    @classmethod
    def extract_fields(cls, raw_text: str, field_names: Sequence[str]) -> Dict[str, Optional[str]]:
        if cls.service_available():
            try:
                return cls._extract_with_llm(raw_text, field_names)
            except Exception:
                return FieldExtractor.extract_fields(raw_text)

        return FieldExtractor.extract_fields(raw_text)

    @classmethod
    def _extract_with_llm(cls, raw_text: str, field_names: Sequence[str]) -> Dict[str, Optional[str]]:
        system_message = {
            "role": "system",
            "content": (
                "You are an extraction assistant. "
                "Read the raw shipment document text and return a JSON object with the requested fields. "
                "Only return valid JSON without additional explanation. "
                "If a field cannot be found, set its value to null."
            ),
        }

        request = {
            "role": "user",
            "content": (
                "Extract the following shipment fields from the raw text exactly as JSON: "
                f"{', '.join(field_names)}.\n\nRaw text:\n{raw_text}"
            ),
        }

        response = openai.ChatCompletion.create(
            model=cls.MODEL,
            messages=[system_message, request],
            temperature=0.0,
            max_tokens=512,
        )

        raw_response = response.choices[0].message.content.strip()
        try:
            extracted = json.loads(raw_response)
        except json.JSONDecodeError:
            extracted = FieldExtractor.extract_fields(raw_text)

        return {field: extracted.get(field) for field in field_names}
