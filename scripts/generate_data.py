"""Generate deterministic sample transactions."""

from __future__ import annotations

import argparse
import json
import math
import random
from datetime import date, timedelta
from typing import NamedTuple

Category = str
TransactionData = dict[str, object]

CATEGORY_PARAMETERS: dict[Category, tuple[float, float]] = {
    "Groceries": (60.0, 0.35),
    "Dining": (30.0, 0.4),
    "Transport": (25.0, 0.35),
    "Entertainment": (45.0, 0.4),
    "Utilities": (110.0, 0.25),
    "Shopping": (80.0, 0.5),
    "Travel": (400.0, 0.45),
}
MERCHANTS: dict[Category, tuple[str, ...]] = {
    "Groceries": ("Fresh Market", "Neighborhood Foods", "Green Basket"),
    "Dining": ("Corner Cafe", "Pasta House", "The Burger Spot"),
    "Transport": ("City Transit", "Metro Fuel", "Ride Share"),
    "Entertainment": ("Cinema Center", "Game Hub", "Concert Hall"),
    "Utilities": ("City Power", "Water Works", "Home Internet"),
    "Shopping": ("Main Street Shop", "Online Market", "Style Outlet"),
    "Travel": ("Skyline Airlines", "Grand Hotel", "Road Trip Rentals"),
}
CATEGORIES = tuple(CATEGORY_PARAMETERS)


class GeneratedData(NamedTuple):
    """Generated transactions and their zero-based outlier indices."""

    transactions: list[TransactionData]
    outlier_indices: list[int]


def generate_transactions(n: int, seed: int = 42) -> GeneratedData:
    """Generate n deterministic transactions with exactly ten outliers."""
    if n < 10:
        raise ValueError("n must be at least 10 to inject exactly 10 outliers")

    rng = random.Random(seed)
    today = date.today()
    transactions: list[TransactionData] = []

    for _ in range(n):
        category = rng.choice(CATEGORIES)
        median, sigma = CATEGORY_PARAMETERS[category]
        transactions.append(
            {
                "date": today - timedelta(days=rng.randrange(365)),
                "merchant": rng.choice(MERCHANTS[category]),
                "category": category,
                "amount": round(rng.lognormvariate(math.log(median), sigma), 2),
                "description": None,
            }
        )

    outlier_indices = list(range(n - 10, n))
    for index in outlier_indices:
        transaction = transactions[index]
        category = transaction["category"]
        median, _ = CATEGORY_PARAMETERS[category]
        transaction["amount"] = round(median * 5, 2)

    return GeneratedData(transactions, outlier_indices)


def main() -> None:
    """Run the transaction generator CLI."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-n", type=int, default=500, help="number of transactions")
    parser.add_argument("--seed", type=int, default=42, help="random seed")
    args = parser.parse_args()
    generated = generate_transactions(args.n, args.seed)
    print(
        json.dumps(
            {
                "transactions": generated.transactions,
                "outlier_indices": generated.outlier_indices,
            },
            default=str,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
