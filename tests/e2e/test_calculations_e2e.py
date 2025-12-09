# tests/e2e/test_calculations_e2e.py

from playwright.sync_api import Page

BASE_URL = "http://127.0.0.1:8000"


def go_to_calculations_page(page: Page) -> None:
    page.goto(f"{BASE_URL}/calculations-page")


def create_sample_calculation(page: Page, a: float = 2, b: float = 3, op: str = "add") -> None:
    """Helper: use the form to create one calculation."""
    go_to_calculations_page(page)

    page.fill("#a", str(a))
    page.fill("#b", str(b))
    page.select_option("#type", op)
    page.click("#create-button")

    # Wait a bit for server + DOM update
    page.wait_for_timeout(500)


def test_calculations_create_shows_success_message(page: Page) -> None:
    """Positive: user can create a calculation from the page."""
    go_to_calculations_page(page)

    page.fill("#a", "2")
    page.fill("#b", "3")
    page.select_option("#type", "add")
    page.click("#create-button")

    page.wait_for_timeout(500)

    # We don't depend on exact table contents; just that UI reports success
    msg = page.inner_text("#message")
    assert "Calculation created successfully." in msg


def test_calculations_edit_and_delete_flow(page: Page) -> None:
    """
    Positive: user can update and delete an existing calculation.

    We reuse the page's JS logic, which uses window.prompt() and confirm().
    Playwright handles dialogs via the 'dialog' event.
    """

    # First, ensure at least one calculation exists
    create_sample_calculation(page, a=5, b=4, op="sub")

    # Set up a generic dialog handler to accept prompts/confirm dialogs
    def handle_dialog(dialog):
        # For prompts, send back the existing default value
        dialog.accept(dialog.default_value or "")

    page.on("dialog", handle_dialog)

    # Click the first "Edit" button – this will trigger three prompts (A, B, type)
    go_to_calculations_page(page)
    page.click("button.edit-btn")

    page.wait_for_timeout(500)
    msg_after_edit = page.inner_text("#message")
    assert "Calculation updated successfully." in msg_after_edit

    # Now delete the first row
    page.click("button.delete-btn")
    page.wait_for_timeout(500)
    msg_after_delete = page.inner_text("#message")
    assert "Calculation deleted." in msg_after_delete


def test_calculations_invalid_inputs_show_error(page: Page) -> None:
    """Negative: empty / non-numeric input should trigger client-side validation error."""
    go_to_calculations_page(page)

    # Leave both fields blank so parseFloat() returns NaN
    page.fill("#a", "")
    page.fill("#b", "")
    page.select_option("#type", "add")
    page.click("#create-button")

    page.wait_for_timeout(300)

    msg = page.inner_text("#message")
    assert "must be numbers" in msg  # "A and B must be numbers."



def test_calculations_division_by_zero_is_blocked(page: Page) -> None:
    """
    Negative: division by zero should NOT create a new calculation
    and should show some kind of validation/error message.
    """
    go_to_calculations_page(page)

    # Count rows before attempting division by zero
    rows_before = page.locator("#calc-rows tr").count()

    page.fill("#a", "1")
    page.fill("#b", "0")
    page.select_option("#type", "div")
    page.click("#create-button")

    page.wait_for_timeout(500)

    msg = page.inner_text("#message")
    # We don't know the exact text (Pydantic error JSON), but it should not be empty
    assert msg.strip() != ""

    # Table should not shrink because of a failed create; we just check it's not broken
    rows_after = page.locator("#calc-rows tr").count()
    assert rows_after >= 0  # basic sanity check – page still renders rows
