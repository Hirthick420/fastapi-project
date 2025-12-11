# tests/integration/test_calculation_routes.py

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_calculation_crud_round_trip():
    # 1) Create a calculation
    create_payload = {"a": 2, "b": 3, "type": "add"}

    create_resp = client.post("/calculations", json=create_payload)
    assert create_resp.status_code == 201

    created = create_resp.json()
    calc_id = created["id"]

    assert created["a"] == 2
    assert created["b"] == 3
    assert created["type"] == "add"
    # 2 + 3 = 5
    assert created["result"] == 5
    # user_id is optional; in your schema it may be null/None
    assert "user_id" in created

    # 2) Read it back
    get_resp = client.get(f"/calculations/{calc_id}")
    assert get_resp.status_code == 200

    fetched = get_resp.json()
    assert fetched == created  # same data as when it was created

    # 3) Update (Edit) the calculation
    update_payload = {"a": 10, "b": 4, "type": "mul"}

    update_resp = client.put(f"/calculations/{calc_id}", json=update_payload)
    assert update_resp.status_code == 200

    updated = update_resp.json()
    assert updated["id"] == calc_id
    assert updated["a"] == 10
    assert updated["b"] == 4
    assert updated["type"] == "mul"
    # 10 * 4 = 40
    assert updated["result"] == 40

    # 4) Browse (list) calculations – should include our updated one
    list_resp = client.get("/calculations")
    assert list_resp.status_code == 200

    items = list_resp.json()
    assert isinstance(items, list)
    assert any(item["id"] == calc_id for item in items)

    # 5) Delete calculation
    delete_resp = client.delete(f"/calculations/{calc_id}")
    assert delete_resp.status_code in (200, 204)

    # 6) Reading again should now give 404
    get_after_delete = client.get(f"/calculations/{calc_id}")
    assert get_after_delete.status_code == 404


def test_division_by_zero_validation_error():
    # This should be blocked by your Pydantic validator in CalculationCreate
    bad_payload = {"a": 1, "b": 0, "type": "div"}

    resp = client.post("/calculations", json=bad_payload)
    # Pydantic validation error => 422 Unprocessable Entity
    assert resp.status_code == 422
    body = resp.json()
    assert "detail" in body


def test_power_calculation_route():
    """
    Ensure advanced 'power' operation works end-to-end via the /calculations route.
    """
    payload = {"a": 2, "b": 3, "type": "power"}

    resp = client.post("/calculations", json=payload)
    assert resp.status_code == 201

    data = resp.json()
    assert data["a"] == 2
    assert data["b"] == 3
    assert data["type"] == "power"
    assert data["result"] == 8  # 2 ** 3 = 8


def test_log_invalid_base_validation_error():
    """
    Logarithm with invalid base (b == 1) should fail Pydantic validation and return 422.
    """
    bad_payload = {"a": 10, "b": 1, "type": "log"}

    resp = client.post("/calculations", json=bad_payload)
    assert resp.status_code == 422

    body = resp.json()
    assert "detail" in body
    # Optional: check that our error message about base is in the details
    error_messages = str(body["detail"])
    assert "Logarithm base must be > 0 and != 1" in error_messages
