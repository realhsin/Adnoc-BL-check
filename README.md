# Shipment Comparison Engine

A Python project for extracting shipment data from DOCX/PDF documents, normalizing fields, and comparing shipment records.

## Features

- Domain model for shipment data
- Comparison engine for matched, mismatched, missing, and invalid fields
- DOCX and PDF document loading
- Field extraction and normalization
- Streamlit web UI for document upload and comparison
- AI-enhanced extraction fallback when `OPENAI_API_KEY` is available
- Fuzzy matching suggestions for ports, commodities, and container types
- Downloadable JSON comparison reports

## Installation

```bash
cd '/Users/husain/Library/CloudStorage/OneDrive-UAEUniversity/Courses/Year 4/Spring 2026/Internship/Adnoc/Project/Script'
python3 -m pip install --quiet -r requirements.txt
```

> If `requirements.txt` is not present, install the dependencies manually:

```bash
python3 -m pip install --quiet pytest python-docx pdfminer.six python-dateutil fpdf streamlit openai
```

## Running tests

```bash
cd '/Users/husain/Library/CloudStorage/OneDrive-UAEUniversity/Courses/Year 4/Spring 2026/Internship/Adnoc/Project/Script'
PYTHONPATH=src python3 -m pytest -q
```

## Running the comparison script

```bash
cd '/Users/husain/Library/CloudStorage/OneDrive-UAEUniversity/Courses/Year 4/Spring 2026/Internship/Adnoc/Project/Script'
PYTHONPATH=src python3 run_comparison.py left.docx right.docx
```

## Running the Streamlit app

```bash
cd '/Users/husain/Library/CloudStorage/OneDrive-UAEUniversity/Courses/Year 4/Spring 2026/Internship/Adnoc/Project/Script'
PYTHONPATH=src streamlit run streamlit_app.py
```

### Optional AI extraction

If you want LLM-assisted extraction, set your OpenAI key first:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Then start the Streamlit app again.

## Project structure

- `src/comparison_engine/domain/models/shipment.py` — shipment data model
- `src/comparison_engine/use_cases/compare_shipments.py` — comparison engine
- `src/comparison_engine/adapters/document_loader.py` — DOCX/PDF loaders
- `src/comparison_engine/transformers/field_extractor.py` — text-to-field extraction
- `src/comparison_engine/transformers/normalizer.py` — data normalization
- `src/comparison_engine/transformers/ai_extractor.py` — optional LLM extraction
- `src/comparison_engine/transformers/fuzzy_matcher.py` — fuzzy field suggestions
- `src/comparison_engine/services/report_generator.py` — report builder
- `src/comparison_engine/services/suggestion_service.py` — correction suggestions
- `src/comparison_engine/pipelines/document_pipeline.py` — extraction/comparison flow
- `streamlit_app.py` — web UI
- `run_comparison.py` — CLI comparison script
- `tests/` — unit tests

## Notes

- The current extractor uses regex-based parsing for document fields.
- The project is designed to be extended to handle more shipping line formats and document layouts.
- The Streamlit app displays extracted values, comparison results, and allows report download.
