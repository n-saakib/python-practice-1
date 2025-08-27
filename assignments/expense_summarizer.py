import argparse
import csv
from pathlib import Path
import sys


def get_expenses(path: str) -> tuple[list[dict], int]:
    expense_list = []
    invalid_rows = 0

    with open(path, mode="r", encoding="utf-8", newline="") as fl:
        reader = csv.DictReader(fl)
        for row in reader:
            try:
                category = row.get("category")
                amount_str = row.get("amount")

                if not category or not amount_str:
                    invalid_rows += 1
                    continue

                amount = float(amount_str)

                data = {
                    "category": category,
                    "amount": amount,
                    "date": row.get("date") or "",
                }
                expense_list.append(data)

            except:
                invalid_rows += 1
                continue

    return expense_list, invalid_rows


def summarize_expense(expense_list: list[dict]) -> dict[str, float]:
    summary = {}
    for expense in expense_list:
        category = expense["category"]
        amount = expense["amount"]
        summary[category] = summary.get(category, 0) + amount

    return summary


def filter_expenses(expenses: list[dict], category_filter: str) -> list[dict]:
    return [
        exp
        for exp in expenses
        if exp["category"].lower() == category_filter.strip().lower()
    ]


def sort_summary(
    summary_list: list[tuple[str, float]], sort_by: str
) -> list[tuple[str, float]]:
    if sort_by == "amount_desc":
        summary_list.sort(key=lambda item: item[1], reverse=True)
    elif sort_by == "amount_asc":
        summary_list.sort(key=lambda item: item[1])
    elif sort_by == "category":
        summary_list.sort(key=lambda item: item[0])
    return summary_list


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("--path", type=Path, required=True)
    parser.add_argument(
        "--sort",
        choices=["amount_asc", "amount_desc", "category"],
        default="amount_desc",
    )
    parser.add_argument("--top", type=int)
    parser.add_argument("--filter", type=str)

    args = parser.parse_args()

    try:
        expense_list, invalid_rows = get_expenses(args.path)
        if invalid_rows > 0:
            print(f"Skipped { invalid_rows } invalid rows.", file=sys.stderr)

    except Exception as e:
        print(f"Error: { e }", file=sys.stderr)
        sys.exit(1)

    if args.filter:
        try:
            filter_key, filter_value = args.filter.split("=", 1)
            if filter_key.strip().lower() == "category":
                expense_list = filter_expenses(expense_list, filter_value)
            else:
                print(
                    f"Warning: Only filtering by 'category' is supported.",
                    file=sys.stderr,
                )
        except Exception as e:
            print(f"Error: { e }", file=sys.stderr)
            sys.exit(1)

    if not expense_list:
        print("No data to display.")
        return

    summary_list = list(summarize_expense(expense_list).items())
    summary_list = sort_summary(summary_list, args.sort)

    if args.top is not None:
        summary_list = summary_list[: args.top]

    print(f"{'category':<15} {'total':>10}")
    print("-" * 26)
    for category, total in summary_list:
        print(f"{category:<15} {total:>10.2f}")


if __name__ == "__main__":
    main()
