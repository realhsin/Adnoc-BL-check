from __future__ import annotations
import json
import sys
from pathlib import Path

from comparison_engine.pipelines.document_pipeline import DocumentPipeline
from comparison_engine.services.report_generator import ReportGenerator


def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: python3 run_comparison.py <left.docx|left.pdf> <right.docx|right.pdf>")
        return 1

    left_path = Path(sys.argv[1])
    right_path = Path(sys.argv[2])

    if not left_path.exists() or not right_path.exists():
        print("Error: both input files must exist.")
        return 1

    comparison = DocumentPipeline.compare_document_pair(str(left_path), str(right_path))
    left_shipment = comparison["left_shipment"]
    right_shipment = comparison["right_shipment"]
    report = ReportGenerator.build_report(comparison["report"])

    output = {
        "left_shipment": left_shipment.to_dict(),
        "right_shipment": right_shipment.to_dict(),
        "report": report,
    }

    print(json.dumps(output, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
