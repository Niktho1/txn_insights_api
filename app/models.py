"""Database models."""

from datetime import date

from sqlalchemy import CheckConstraint, Date, Float, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db import Base


class Transaction(Base):
    """A bank transaction."""

    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint(
            "category IN ('Groceries', 'Dining', 'Transport', "
            "'Entertainment', 'Utilities', 'Shopping', 'Travel')",
            name="ck_transactions_category",
        ),
        CheckConstraint("amount > 0", name="ck_transactions_amount_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    date: Mapped[date] = mapped_column(Date, nullable=False)
    merchant: Mapped[str] = mapped_column(String, nullable=False)
    category: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)
    description: Mapped[str | None] = mapped_column(String, nullable=True)
