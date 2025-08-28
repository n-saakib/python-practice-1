import pytest
from decimal import Decimal

from assignments.bank_ledger.bank_account import BankAccount, load_transactions


@pytest.fixture
def account():
    return BankAccount(owner="Test User", balance=Decimal("100.00"))


# --- Tests for BankAccount Class ---


def test_account_creation():
    """Tests basic attributes of a new BankAccount."""
    acc = BankAccount(owner="Alice", balance=Decimal("50.75"))
    assert acc.owner == "Alice"
    assert acc.balance == Decimal("50.75")
    assert acc.statement() == []


def test_apply_deposit(account):
    """Tests that a deposit correctly increases the balance."""
    tx = {"type": "deposit", "amount": Decimal("50.00"), "note": "paycheck"}
    account.apply(tx)
    assert account.balance == Decimal("150.00")
    assert len(account.statement()) == 1
    assert account.statement()[0][1:] == (
        "deposit",
        Decimal("50.00"),
        Decimal("150.00"),
        "paycheck",
    )


def test_apply_withdraw_success(account):
    """Tests that a valid withdrawal correctly decreases the balance."""
    tx = {"type": "withdraw", "amount": Decimal("25.50"), "note": "groceries"}
    account.apply(tx)
    assert account.balance == Decimal("74.50")
    assert len(account.statement()) == 1


def test_apply_withdraw_insufficient_funds(account):
    """Tests that a withdrawal larger than the balance raises a ValueError."""
    tx = {"type": "withdraw", "amount": Decimal("1000.00"), "note": "rent"}
    with pytest.raises(ValueError, match="Invalid Transaction. Insufficient Balance"):
        account.apply(tx)
    assert account.balance == Decimal("100.00")
    assert len(account.statement()) == 0


def test_apply_invalid_transaction_type(account):
    """Tests that an unknown transaction type raises a ValueError."""
    tx = {"type": "invoice", "amount": Decimal("50.00"), "note": "invalid"}
    with pytest.raises(ValueError, match="Invalid Transaction Type invoice"):
        account.apply(tx)


# --- Tests for load_transactions ---


def test_load_transactions_success(tmp_path):
    """Tests loading a well-formed transaction CSV."""
    p = tmp_path / "transactions.csv"
    p.write_text(
        "type,amount,note\n"
        "deposit,100.00,initial funding\n"
        "withdraw,25.55,coffee & snacks\n"
    )
    transactions = load_transactions(p)
    assert len(transactions) == 2
    assert transactions[0] == {
        "type": "deposit",
        "amount": Decimal("100.00"),
        "note": "initial funding",
    }
    assert transactions[1] == {
        "type": "withdraw",
        "amount": Decimal("25.55"),
        "note": "coffee & snacks",
    }


def test_load_transactions_invalid_amount(tmp_path):
    """Tests that an invalid amount in the CSV raises a ValueError."""
    p = tmp_path / "bad_transactions.csv"
    p.write_text("type,amount,note\ndeposit,NOT_A_NUMBER,fail\n")
    with pytest.raises(ValueError):
        load_transactions(p)
