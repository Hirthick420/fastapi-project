# tests/unit/test_report_schemas.py
from app.schemas.report import ReportSummary


def test_report_summary_schema_basic():
    summary = ReportSummary(
        total_calculations=3,
        counts_by_type={"add": 2, "power": 1},
        average_a=5.0,
        average_b=7.0,
        most_used_type="add",
        last_calculation_id=10,
    )

    assert summary.total_calculations == 3
    assert summary.counts_by_type["add"] == 2
    assert summary.most_used_type == "add"
    assert summary.last_calculation_id == 10
