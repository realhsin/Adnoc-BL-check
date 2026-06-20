from __future__ import annotations
import difflib
from typing import Iterable, List, Optional


class FuzzyMatcher:
    KNOWN_PORTS: List[str] = [
        "Dubai",
        "Abu Dhabi",
        "Shanghai",
        "Rotterdam",
        "Singapore",
        "Hamburg",
        "Los Angeles",
        "New York",
        "Jebel Ali",
        "Ruwais",
    ]

    KNOWN_CONTAINER_TYPES: List[str] = [
        "Dry",
        "Reefer",
        "40HC",
        "20FT",
        "40FT",
        "Open Top",
        "Flat Rack",
        "ISO Tank",
    ]

    KNOWN_COMMODITIES: List[str] = [
        "Polyethylene Resin",
        "Electronics",
        "Textiles",
        "Steel",
        "Automotive Parts",
        "Pharmaceuticals",
        "Furniture",
        "Food Products",
    ]

    @classmethod
    def suggest_port_name(cls, value: str) -> Optional[str]:
        return cls._suggest(value, cls.KNOWN_PORTS)

    @classmethod
    def suggest_container_type(cls, value: str) -> Optional[str]:
        return cls._suggest(value, cls.KNOWN_CONTAINER_TYPES)

    @classmethod
    def suggest_commodity(cls, value: str) -> Optional[str]:
        return cls._suggest(value, cls.KNOWN_COMMODITIES)

    @classmethod
    def _suggest(cls, value: str, choices: Iterable[str]) -> Optional[str]:
        if not value:
            return None

        normalized = value.strip().casefold()
        choice_map = {choice.casefold(): choice for choice in choices}
        close = difflib.get_close_matches(normalized, list(choice_map.keys()), n=1, cutoff=0.6)
        if close:
            return choice_map[close[0]]

        return None
