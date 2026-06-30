# ACE-EXPECT: detect
# CATEGORY: should_detect/tool_idempotency
# LANGUAGE: python
# ISSUE: A create-order tool inserts a new DB row with no idempotency key and runs inside an agent retry loop, duplicating orders
# EXPECTED-FINDING: A retry after a transient commit/connection error inserts a second identical order row; there is no unique constraint or dedup key to prevent it
# EXPECTED-FIX: Derive an idempotency key from the request and enforce it via a UNIQUE column + INSERT ... ON CONFLICT DO NOTHING (or check-then-skip) so retries don't duplicate
# SEVERITY-HINT: warning
"""A create_order tool backed by SQLAlchemy for an ordering agent that retries."""

import time

from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, nullable=False)
    sku = Column(String, nullable=False)
    qty = Column(Integer, nullable=False)


engine = create_engine("postgresql://localhost/shop")
Session = sessionmaker(bind=engine)


def create_order(customer_id: str, sku: str, qty: int) -> int:
    """Insert an order row and return its new id."""
    session = Session()
    # No idempotency key — every call inserts a fresh autoincrement row.
    order = Order(customer_id=customer_id, sku=sku, qty=qty)
    session.add(order)
    session.commit()
    return order.id


def create_order_tool(customer_id: str, sku: str, qty: int) -> int:
    """Agent tool wrapper that retries the insert on transient DB errors."""
    for attempt in range(3):
        try:
            return create_order(customer_id, sku, qty)
        except OperationalError:
            time.sleep(2**attempt)
    raise RuntimeError("create_order failed after retries")
