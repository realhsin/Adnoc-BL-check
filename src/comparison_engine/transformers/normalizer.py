from __future__ import annotations
import re
from datetime import datetime
from typing import Dict, Optional

from dateutil.parser import parse as parse_date


class FieldNormalizer:
    CONTAINER_TYPE_MAP: Dict[str, str] = {
        "dry": "Dry",
        "20ft dry": "Dry",
        "40ft dry": "Dry",
        "reefer": "Reefer",
        "refrigerated": "Reefer",
    }

    PORT_NAME_MAP: Dict[str, str] = {
        "dxb": "Dubai",
        "dubai": "Dubai",
        "jebel ali": "Dubai",
        "abudhabi": "Abu Dhabi",
        "abu dhabi": "Abu Dhabi",
        "auh": "Abu Dhabi",
    }

    @classmethod
    def normalize(cls, extracted: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        normalized: Dict[str, Optional[str]] = {}

        for field_name, value in extracted.items():
            if value is None:
                normalized[field_name] = None
                continue

            if field_name in {"quantity", "gross_weight", "net_weight"}:
                normalized[field_name] = cls._normalize_numeric_value(value)
            elif field_name == "container_type":
                normalized[field_name] = cls._normalize_container_type(value)
            elif field_name in {"origin", "destination"}:
                normalized[field_name] = cls._normalize_port_name(value)
            elif cls._looks_like_date(field_name, value):
                normalized[field_name] = cls._normalize_date(value)
            else:
                normalized[field_name] = value.strip()

        return normalized

    @staticmethod
    def _normalize_numeric_value(value: str) -> Optional[str]:
        cleaned = value.replace(",", "").strip()
        cleaned = re.sub(r"[^0-9\.\-]+", "", cleaned)
        if cleaned == "":
            return None

        try:
            number = float(cleaned)
        except ValueError:
            return value.strip()

        if number.is_integer():
            return str(int(number))
        return str(number)

    @classmethod
    def _normalize_container_type(cls, value: str) -> str:
        key = value.strip().casefold()
        return cls.CONTAINER_TYPE_MAP.get(key, value.strip().title())

    @classmethod
    def _normalize_port_name(cls, value: str) -> str:
        key = value.strip().casefold()
        return cls.PORT_NAME_MAP.get(key, value.strip().title())

    @staticmethod
    def _looks_like_date(field_name: str, value: str) -> bool:
        return "date" in field_name or any(keyword in value.lower() for keyword in ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec", "/", "-"])

    @staticmethod
    def _normalize_date(value: str) -> Optional[str]:
        try:
            parsed = parse_date(value, dayfirst=False)
            return parsed.strftime("%Y-%m-%d")
        except (ValueError, OverflowError):
            return value.strip()
