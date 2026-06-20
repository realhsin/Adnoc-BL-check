from __future__ import annotations
from typing import Dict, Optional

from comparison_engine.transformers.fuzzy_matcher import FuzzyMatcher


class SuggestionService:
    @staticmethod
    def build_suggestions(extracted: Dict[str, Optional[str]]) -> Dict[str, Optional[str]]:
        suggestions: Dict[str, Optional[str]] = {}

        for field_name, value in extracted.items():
            if value is None:
                continue

            if field_name in {"origin", "destination"}:
                suggestion = FuzzyMatcher.suggest_port_name(value)
            elif field_name == "container_type":
                suggestion = FuzzyMatcher.suggest_container_type(value)
            elif field_name == "commodity":
                suggestion = FuzzyMatcher.suggest_commodity(value)
            else:
                suggestion = None

            if suggestion and suggestion.casefold() != value.strip().casefold():
                suggestions[field_name] = suggestion

        return suggestions
