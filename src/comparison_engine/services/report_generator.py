from __future__ import annotations
from typing import Any, Dict

from comparison_engine.use_cases.compare_shipments import ComparisonDetail, ComparisonResult


class ReportGenerator:
    @staticmethod
    def build_report(result: ComparisonResult) -> Dict[str, Any]:
        return {
            "matched_fields": result.matched_fields,
            "mismatched_fields": [
                {
                    "field_name": detail.field_name,
                    "left_value": detail.left_value,
                    "right_value": detail.right_value,
                    "reason": detail.reason,
                }
                for detail in result.mismatched_fields
            ],
            "missing_fields": [
                {
                    "field_name": detail.field_name,
                    "left_value": detail.left_value,
                    "right_value": detail.right_value,
                    "reason": detail.reason,
                }
                for detail in result.missing_fields
            ],
            "invalid_fields": [
                {
                    "field_name": detail.field_name,
                    "left_value": detail.left_value,
                    "right_value": detail.right_value,
                    "reason": detail.reason,
                }
                for detail in result.invalid_fields
            ],
            "summary": result.summary,
        }
