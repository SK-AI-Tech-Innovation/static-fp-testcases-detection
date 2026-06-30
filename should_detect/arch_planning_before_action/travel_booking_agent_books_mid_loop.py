# ACE-EXPECT: detect
# CATEGORY: should_detect/arch_planning_before_action
# LANGUAGE: python
# ISSUE: Travel agent calls real booking APIs mid-loop with no itinerary plan or confirmation step
# EXPECTED-FINDING: Flight/hotel bookings (irreversible side effects) are committed inside the tool loop with no plan-then-confirm separation
# EXPECTED-FIX: Generate a complete proposed itinerary, surface it for validation/approval, then book in a dedicated execute phase
# SEVERITY-HINT: warning
"""A 'book my trip' agent that charges the card the moment the model picks an option."""

import json

from anthropic import Anthropic

client = Anthropic()


def book_flight(flight_id: str) -> dict:
    return {"booked": flight_id, "status": "confirmed"}


def book_hotel(hotel_id: str) -> dict:
    return {"booked": hotel_id, "status": "confirmed"}


TOOLS = [
    {"name": "book_flight", "description": "Book and pay for a flight",
     "input_schema": {"type": "object", "properties": {"flight_id": {"type": "string"}}}},
    {"name": "book_hotel", "description": "Book and pay for a hotel",
     "input_schema": {"type": "object", "properties": {"hotel_id": {"type": "string"}}}},
]


def plan_trip(request: str) -> list[dict]:
    results = []
    messages = [{"role": "user", "content": request}]
    while True:
        resp = client.messages.create(model="claude-opus-4-20250514", max_tokens=1024, tools=TOOLS, messages=messages)
        tool_uses = [b for b in resp.content if b.type == "tool_use"]
        if not tool_uses:
            return results
        for tu in tool_uses:
            # books and pays instantly during the loop — no itinerary plan, no user confirmation
            out = book_flight(**tu.input) if tu.name == "book_flight" else book_hotel(**tu.input)
            results.append(out)
            messages.append({"role": "user", "content": json.dumps(out)})
