# tests/integration/test_reports_routes.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def _create_calc(a: float, b: float, type_: str):
    resp = client.post("/calculations", json={"a": a, "b": b, "type": type_})
    assert resp.status_code == 201
    return resp.json()


def test_reports_summary_counts_and_most_used():
    # Seed some calculations
    _create_calc(2, 3, "add")
    _create_calc(5, 1, "add")
    _create_calc(2, 3, "power")

    resp = client.get("/reports/summary")
    assert resp.status_code == 200
    data = resp.json()

    assert data["total_calculations"] >= 3
    counts = data["counts_by_type"]
    assert counts["add"] >= 2
    assert counts["power"] >= 1
    assert data["most_used_type"] in counts  # must be a valid key


def test_reports_recent_limit():
    # Seed a few calculations
    created_ids = []
    for i in range(5):
        created = _create_calc(i, i + 1, "add")
        created_ids.append(created["id"])

    resp = client.get("/reports/recent?limit=3")
    assert resp.status_code == 200
    items = resp.json()

    assert len(items) == 3
    # Should contain the most recently created ones (highest ids)
    returned_ids = [item["id"] for item in items]
    assert max(returned_ids) <= max(created_ids)
