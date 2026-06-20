from comparison_engine.domain.models.shipment import Shipment
from comparison_engine.services.report_generator import ReportGenerator
from comparison_engine.use_cases.compare_shipments import CompareShipments


def test_compare_shipments_all_fields_match():
    left = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )
    right = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100.0",
        gross_weight="2000.00",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )

    result = CompareShipments.compare(left, right)
    report = ReportGenerator.build_report(result)

    assert result.summary["total_fields"] == 11
    assert result.summary["matched_fields"] == 11
    assert result.summary["mismatched_fields"] == 0
    assert result.summary["missing_fields"] == 0
    assert result.summary["invalid_fields"] == 0
    assert report["matched_fields"] == [
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
    ]


def test_compare_shipments_detects_missing_and_different_values():
    left = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="Dry",
        origin="",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )
    right = Shipment(
        bl_number="BL999",
        container_number="CONT001",
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )

    result = CompareShipments.compare(left, right)
    assert result.summary["total_fields"] == 11
    assert result.summary["matched_fields"] == 9
    assert result.summary["mismatched_fields"] == 1
    assert result.summary["missing_fields"] == 1
    assert result.summary["invalid_fields"] == 0

    assert result.mismatched_fields[0].field_name == "bl_number"
    assert result.missing_fields[0].field_name == "origin"


def test_compare_shipments_detects_invalid_values():
    left = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="one hundred",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )
    right = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="two thousand",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )

    result = CompareShipments.compare(left, right)
    assert result.summary["invalid_fields"] == 2
    assert {detail.field_name for detail in result.invalid_fields} == {"quantity", "gross_weight"}


def test_report_generator_returns_full_summary():
    left = Shipment(
        bl_number="BL123",
        container_number="CONT001",
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )
    right = Shipment(
        bl_number="BL123",
        container_number=None,
        container_type="Dry",
        origin="Dubai",
        destination="Abu Dhabi",
        commodity="Electronics",
        quantity="100",
        gross_weight="2000",
        net_weight="1800",
        vessel="VesselA",
        voyage="V001",
    )

    result = CompareShipments.compare(left, right)
    report = ReportGenerator.build_report(result)

    assert report["summary"]["total_fields"] == 11
    assert report["summary"]["missing_fields"] == 1
    assert report["missing_fields"][0]["field_name"] == "container_number"
