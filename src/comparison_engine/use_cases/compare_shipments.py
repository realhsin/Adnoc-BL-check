from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from comparison_engine.domain.models.shipment import Shipment


@dataclass
class ComparisonDetail:
    field_name: str
    left_value: Optional[str]
    right_value: Optional[str]
    reason: Optional[str] = None


@dataclass
class ComparisonResult:
    matched_fields: List[str]
    mismatched_fields: List[ComparisonDetail]
    missing_fields: List[ComparisonDetail]
    invalid_fields: List[ComparisonDetail]
    summary: Dict[str, int]


class CompareShipments:
    @staticmethod
    def _is_missing(value: Optional[str]) -> bool:
        return value is None or str(value).strip() == ""

    @staticmethod
    def _is_invalid(field_name: str, value: Optional[str]) -> bool:
        if value is None:
            return False

        if field_name in Shipment.NUMERIC_FIELDS:
            normalized = str(value).strip()
            if normalized == "":
                return False
            try:
                float(normalized)
                return False
            except ValueError:
                return True

        return False

    @classmethod
    def compare(cls, left: Shipment, right: Shipment) -> ComparisonResult:
        matched_fields: List[str] = []
        mismatched_fields: List[ComparisonDetail] = []
        missing_fields: List[ComparisonDetail] = []
        invalid_fields: List[ComparisonDetail] = []

        for field_name in Shipment.FIELDS:
            left_value = getattr(left, field_name)
            right_value = getattr(right, field_name)
            left_missing = cls._is_missing(left_value)
            right_missing = cls._is_missing(right_value)

            if left_missing or right_missing:
                missing_fields.append(
                    ComparisonDetail(
                        field_name=field_name,
                        left_value=left_value,
                        right_value=right_value,
                        reason="missing value",
                    )
                )
                continue

            left_invalid = cls._is_invalid(field_name, left_value)
            right_invalid = cls._is_invalid(field_name, right_value)
            if left_invalid or right_invalid:
                reason = "invalid numeric value" if field_name in Shipment.NUMERIC_FIELDS else "invalid value"
                invalid_fields.append(
                    ComparisonDetail(
                        field_name=field_name,
                        left_value=left_value,
                        right_value=right_value,
                        reason=reason,
                    )
                )
                continue

            normalized_left = left.normalized_value(field_name)
            normalized_right = right.normalized_value(field_name)

            if normalized_left == normalized_right:
                matched_fields.append(field_name)
            else:
                mismatched_fields.append(
                    ComparisonDetail(
                        field_name=field_name,
                        left_value=left_value,
                        right_value=right_value,
                        reason="different value",
                    )
                )

        summary = {
            "total_fields": len(Shipment.FIELDS),
            "matched_fields": len(matched_fields),
            "mismatched_fields": len(mismatched_fields),
            "missing_fields": len(missing_fields),
            "invalid_fields": len(invalid_fields),
            "valid_comparisons": len(matched_fields) + len(mismatched_fields),
        }

        return ComparisonResult(
            matched_fields=matched_fields,
            mismatched_fields=mismatched_fields,
            missing_fields=missing_fields,
            invalid_fields=invalid_fields,
            summary=summary,
        )
