# tests/e2e/test_reports_e2e.py

BASE_URL = "http://127.0.0.1:8000"


def test_reports_page_shows_summary_and_recent(page, browser_name):
    # 1) Create at least one calculation via the existing UI
    page.goto(f"{BASE_URL}/calculations-page")

    page.fill("#a", "2")
    page.fill("#b", "3")
    page.select_option("#type", "add")
    page.click("#create-button")

    # Give the backend a moment to save & page to refresh table
    page.wait_for_timeout(500)

    # 2) Go to reports page
    page.goto(f"{BASE_URL}/reports-page")

    # 3) Check that summary text appears
    page.wait_for_timeout(500)
    body_text = page.text_content("body")
    assert "Total calculations:" in body_text

    # 4) Ensure recent calculations table shows at least one 'add' row
    recent_text = page.text_content("tbody#recent-rows")
    assert "add" in recent_text
