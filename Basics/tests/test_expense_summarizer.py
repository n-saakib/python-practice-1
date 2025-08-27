import pytest

from expense_summarizer import (
    get_expenses,
    summarize_expense,
    filter_expenses,
    sort_summary,
)

# --- Sample Data for Re-use in Tests ---
SAMPLE_EXPENSES = [
    {"category": "food", "amount": 10.0, "date": ""},
    {"category": "travel", "amount": 100.0, "date": ""},
    {"category": "food", "amount": 25.50, "date": ""},
    {"category": "misc", "amount": 5.0, "date": ""},
    {"category": "travel", "amount": 50.0, "date": ""},
]

# --- Tests for get_expenses ---


def test_get_expenses_success(tmp_path):
    """Tests loading a well-formed CSV file."""
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "expenses.csv"
    p.write_text(
        "category,amount,date\n"
        "food,12.50,2025-08-01\n"
        "travel,100,2025-08-03\n"
        "food,30,\n"
    )
    expenses, skipped = get_expenses(p)
    assert skipped == 0
    assert len(expenses) == 3
    assert expenses[0] == {"category": "food", "amount": 12.50, "date": "2025-08-01"}
    assert expenses[1] == {"category": "travel", "amount": 100.00, "date": "2025-08-03"}
    assert expenses[2] == {"category": "food", "amount": 30.00, "date": ""}


def test_get_expenses_skips_bad_rows(tmp_path):
    """Tests that rows with invalid data are skipped correctly."""
    p = tmp_path / "expenses.csv"
    p.write_text(
        "category,amount,date\n"
        "food,12.50,2025-08-01\n"
        ",50,2025-08-02\n"
        "travel,,2025-08-03\n"
        "misc,INVALID,2025-08-04\n"
        "entertainment,75.00,2025-08-05\n"
    )
    expenses, skipped = get_expenses(p)
    assert skipped == 3
    assert len(expenses) == 2
    assert expenses[0] == {"category": "food", "amount": 12.50, "date": "2025-08-01"}
    assert expenses[1] == {
        "category": "entertainment",
        "amount": 75.00,
        "date": "2025-08-05",
    }


def test_get_expenses_file_not_found():
    """Tests that a FileNotFoundError is raised for a non-existent file."""
    with pytest.raises(FileNotFoundError):
        get_expenses("non_existent_file.csv")


# --- Tests for summarize_expense ---


def test_summarize_expense_success():
    """Tests a standard case of summarizing expenses by category."""
    summary = summarize_expense(SAMPLE_EXPENSES)
    assert summary == {"food": 35.50, "travel": 150.0, "misc": 5.0}


def test_summarize_expense_empty_list():
    """Tests that an empty list of expenses results in an empty summary."""
    assert summarize_expense([]) == {}


# --- Tests for filter_expenses ---


def test_filter_expenses_success():
    """Tests filtering for a category that exists."""
    filtered = filter_expenses(SAMPLE_EXPENSES, "food")
    assert len(filtered) == 2
    assert filtered[0]["category"] == "food"
    assert filtered[1]["category"] == "food"


def test_filter_expenses_no_match():
    """Tests filtering for a category that does not exist."""
    filtered = filter_expenses(SAMPLE_EXPENSES, "shopping")
    assert len(filtered) == 0


def test_filter_expenses_on_empty_list():
    """Tests filtering an already empty list."""
    filtered = filter_expenses([], "food")
    assert len(filtered) == 0


# --- Tests for sort_summary ---


@pytest.fixture
def sample_summary_list():
    """A pytest fixture to provide a sample summary list for sorting tests."""
    return [("travel", 150.0), ("food", 35.50), ("misc", 5.0)]


def test_sort_summary_by_amount_desc(sample_summary_list):
    """Tests sorting by amount in descending order."""
    sorted_list = sort_summary(sample_summary_list, "amount_desc")
    assert [item[0] for item in sorted_list] == ["travel", "food", "misc"]


def test_sort_summary_by_amount_asc(sample_summary_list):
    """Tests sorting by amount in ascending order."""
    sorted_list = sort_summary(sample_summary_list, "amount_asc")
    assert [item[0] for item in sorted_list] == ["misc", "food", "travel"]


def test_sort_summary_by_category(sample_summary_list):
    """Tests sorting by category name alphabetically."""
    sorted_list = sort_summary(sample_summary_list, "category")
    assert [item[0] for item in sorted_list] == ["food", "misc", "travel"]
