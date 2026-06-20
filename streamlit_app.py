import json
import os
import tempfile
from pathlib import Path

import streamlit as st
from comparison_engine.pipelines.document_pipeline import DocumentPipeline
from comparison_engine.services.report_generator import ReportGenerator


def save_uploaded_file(uploaded_file, suffix: str) -> str:
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp_file:
        tmp_file.write(uploaded_file.getbuffer())
        return tmp_file.name


def display_shipment(title: str, shipment_data: dict):
    st.subheader(title)
    st.json(shipment_data)


def display_report(report: dict):
    st.subheader("Comparison Summary")
    st.write(report["summary"])

    st.subheader("Matched Fields")
    st.write(report["matched_fields"])

    if report["mismatched_fields"]:
        st.subheader("Mismatched Fields")
        st.json(report["mismatched_fields"])

    if report["missing_fields"]:
        st.subheader("Missing Fields")
        st.json(report["missing_fields"])

    if report["invalid_fields"]:
        st.subheader("Invalid Fields")
        st.json(report["invalid_fields"])


def main():
    st.set_page_config(page_title="Shipment Comparison UI", layout="wide")
    st.title("Shipment Comparison Application")
    st.markdown(
        "Upload two shipment documents (DOCX or PDF) and compare extracted fields side-by-side. "
        "The app also provides fuzzy suggestions and a downloadable report."
    )

    if os.getenv("OPENAI_API_KEY"):
        st.success("LLM extraction enabled")
    else:
        st.info("LLM extraction disabled: using regex extraction fallback")

    left_file = st.file_uploader("Upload left document", type=["docx", "pdf"], key="left")
    right_file = st.file_uploader("Upload right document", type=["docx", "pdf"], key="right")

    if left_file and right_file:
        left_suffix = Path(left_file.name).suffix
        right_suffix = Path(right_file.name).suffix

        left_path = save_uploaded_file(left_file, left_suffix)
        right_path = save_uploaded_file(right_file, right_suffix)

        comparison = DocumentPipeline.compare_document_pair(left_path, right_path)
        left_shipment = comparison["left_shipment"].to_dict()
        right_shipment = comparison["right_shipment"].to_dict()
        report = ReportGenerator.build_report(comparison["report"])
        left_suggestions = comparison.get("left_suggestions", {})
        right_suggestions = comparison.get("right_suggestions", {})

        col1, col2 = st.columns(2)
        with col1:
            display_shipment("Left Extracted Shipment", left_shipment)
            if left_suggestions:
                st.subheader("Left Correction Suggestions")
                st.json(left_suggestions)

        with col2:
            display_shipment("Right Extracted Shipment", right_shipment)
            if right_suggestions:
                st.subheader("Right Correction Suggestions")
                st.json(right_suggestions)

        display_report(report)

        output = {
            "left_shipment": left_shipment,
            "right_shipment": right_shipment,
            "report": report,
            "left_suggestions": left_suggestions,
            "right_suggestions": right_suggestions,
        }

        report_json = json.dumps(output, indent=2)
        st.download_button(
            "Download comparison report",
            report_json,
            file_name="shipment_comparison_report.json",
            mime="application/json",
        )


if __name__ == "__main__":
    main()
