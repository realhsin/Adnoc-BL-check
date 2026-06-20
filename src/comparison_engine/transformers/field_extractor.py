from __future__ import annotations
import re
from typing import Dict, Optional


class FieldExtractor:
    FIELD_PATTERNS: Dict[str, list[str]] = {
        "bl_number": [
            r"BL\s*(?:Number|No\.?|#)?[:\s]*([A-Za-z0-9\-]+)",
        ],
        "container_number": [
            r"Container\s*(?:Number)?[:\s]*([A-Za-z0-9\-]+)",
        ],
        "container_type": [
            r"Container\s*Type[:\s]*([A-Za-z0-9\s\-]+)",
            r"Type[:\s]*([A-Za-z0-9\s\-]+)",
        ],
        "origin": [
            r"Origin[:\s]*([A-Za-z0-9\s]+)",
        ],
        "destination": [
            r"Destination[:\s]*([A-Za-z0-9\s]+)",
        ],
        "commodity": [
            r"Commodity[:\s]*([A-Za-z0-9\s]+)",
        ],
        "quantity": [
            r"Quantity[:\s]*([0-9,\.\s]+)",
        ],
        "gross_weight": [
            r"Gross\s*Weight[:\s]*([0-9,\.\sA-Za-z]+)",
            r"GW[:\s]*([0-9,\.\sA-Za-z]+)",
        ],
        "net_weight": [
            r"Net\s*Weight[:\s]*([0-9,\.\sA-Za-z]+)",
            r"NW[:\s]*([0-9,\.\sA-Za-z]+)",
        ],
        "vessel": [
            r"Vessel[:\s]*([A-Za-z0-9\s\-]+)",
        ],
        "voyage": [
            r"Voyage[:\s]*([A-Za-z0-9\s\-]+)",
        ],
    }

    @classmethod
    def extract_fields(cls, raw_text: str) -> Dict[str, Optional[str]]:
        extracted: Dict[str, Optional[str]] = {}
        normalized_text = raw_text.replace("\r", "\n")
        lines = [line.strip() for line in normalized_text.splitlines() if line.strip()]

        for field, patterns in cls.FIELD_PATTERNS.items():
            value = None
            for line in lines:
                for pattern in patterns:
                    match = re.search(pattern, line, flags=re.IGNORECASE)
                    if match:
                        value = cls._clean_value(match.group(1))
                        break
                if value is not None:
                    break
            extracted[field] = value

        return extracted

    @staticmethod
    def _clean_value(value: str) -> str:
        cleaned = value.strip()
        cleaned = cleaned.replace("\u00A0", " ")
        cleaned = re.sub(r"\s+", " ", cleaned)
        return cleaned
