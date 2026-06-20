from __future__ import annotations
from dataclasses import dataclass
from typing import ClassVar, Dict, Optional, Sequence


@dataclass
class Shipment:
    bl_number: Optional[str] = None
    container_number: Optional[str] = None
    container_type: Optional[str] = None
    origin: Optional[str] = None
    destination: Optional[str] = None
    commodity: Optional[str] = None
    quantity: Optional[str] = None
    gross_weight: Optional[str] = None
    net_weight: Optional[str] = None
    vessel: Optional[str] = None
    voyage: Optional[str] = None

    FIELDS: ClassVar[Sequence[str]] = (
        "bl_number",
        "container_number",
        "container_type",
        "origin",
        "destination",
        "commodity",
        "quantity",
        "gross_weight",
        "net_weight",
        "vessel",
        "voyage",
    )

    NUMERIC_FIELDS: ClassVar[set[str]] = {"quantity", "gross_weight", "net_weight"}

    def to_dict(self) -> Dict[str, Optional[str]]:
        return {field_name: getattr(self, field_name) for field_name in self.FIELDS}

    def normalized_value(self, field_name: str) -> Optional[str]:
        value = getattr(self, field_name)
        if value is None:
            return None

        normalized = str(value).strip()
        if normalized == "":
            return None

        if field_name in self.NUMERIC_FIELDS:
            try:
                return str(float(normalized))
            except ValueError:
                return normalized

        return normalized.casefold()
