import csv
from dataclasses import dataclass, field
from decimal import Decimal


@dataclass
class BankAccount:
    owner: str
    balance: Decimal = Decimal("0.0")

    _transactions: list[tuple] = field(default_factory=list, repr=False, init=False)

    def apply(self, tx: dict) -> None:
        tx_type = tx.get("type")
        tx_amount = Decimal(tx.get("amount", "0.0"))
        tx_note = tx.get("note", "")

        if tx_type == "deposit":
            self.balance += tx_amount
        elif tx_type == "withdraw":
            if self.balance < tx_amount:
                raise ValueError("Invalid Transaction. Insufficient Balance")
            else:
                self.balance -= tx_amount
        else:
            raise ValueError(f"Invalid Transaction Type {tx_type}")

        tx_index = len(self._transactions)
        self._transactions.append((tx_index, tx_type, tx_amount, self.balance, tx_note))

    def statement(self) -> list[tuple]:
        return self._transactions


def load_transactions(csv_path: str) -> list[dict]:
    transactions = []
    with open(csv_path, mode="r", newline="", encoding="utf-8") as fl:
        reader = csv.DictReader(fl)
        for row in reader:
            try:
                row["amount"] = Decimal(row["amount"])
                transactions.append(row)
            except Exception as e:
                raise ValueError(f"Error: {e}")
    return transactions
