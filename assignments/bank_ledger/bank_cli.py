import argparse
from pathlib import Path
import sys
from decimal import Decimal

from bank_account import BankAccount, load_transactions


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--owner", type=str, required=True)
    parser.add_argument("--balance", type=Decimal, required=True)
    parser.add_argument("--from-csv", dest="csv_path", type=Path, required=True)

    args = parser.parse_args()

    account = BankAccount(owner=args.owner, balance=args.balance)

    try:
        transactions = load_transactions(args.csv_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"Error loading transactions: {e}", file=sys.stderr)
        sys.exit(1)

    try:
        for tx in transactions:
            account.apply(tx)
    except Exception as e:
        print(f"Transaction failed: {e}", file=sys.stderr)
        sys.exit(1)

    print(f"Statement for {account.owner}")
    print("-" * 48)
    print(f"{'ID':<4} {'Type':<10} {'Amount':>10} {'Balance':>12} {'Note'}")
    print("-" * 48)

    for index, tx_type, amount, balance_after, note in account.statement():
        print(
            f"{index:<4} {tx_type:<10} {amount:>10.2f} {balance_after:>12.2f}  {note}"
        )

    print("-" * 48)
    print(f"Final Balance: {account.balance:.2f}")


if __name__ == "__main__":
    main()
