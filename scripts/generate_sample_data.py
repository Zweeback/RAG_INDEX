"""Generate a synthetic ChatGPT conversation export sample for testing."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from random import choice

OUTPUT_PATH = Path("data/raw/chat_export_sample.jsonl")

ROLES = ["user", "assistant", "system"]
BASE_CONTENT = [
    "Discussing project timelines and blockers for the next sprint.",
    "Sharing meeting summary with action items and owners.",
    "Follow-up question about API authentication tokens.",
    "Review of code formatting and linting setup.",
    "Brainstorming marketing copy ideas for landing page.",
]


def build_message(conversation_id: int, index: int, base_time: datetime) -> dict:
    role = ROLES[index % len(ROLES)]
    created_at = base_time + timedelta(minutes=index)
    content = f"[{conversation_id}:{index}] {choice(BASE_CONTENT)}"
    metadata = {
        "model": choice(["gpt-4", "gpt-3.5-turbo", "gpt-4o"]),
        "language": choice(["de", "en"]),
    }
    if index % 13 == 0:
        metadata["tags"] = ["follow-up", "important"]
    if index % 29 == 0:
        metadata["custom_note"] = "Non-ASCII check: Grüße aus München"
    return {
        "conversation_id": f"conv-{conversation_id:04d}",
        "message_index": index,
        "role": role,
        "content": content,
        "created_at": created_at.isoformat(),
        "metadata": metadata,
    }


def main() -> None:
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    base_time = datetime.now(timezone.utc) - timedelta(days=90)
    records = []
    for cid in range(1, 31):
        for idx in range(0, 120):
            records.append(build_message(cid, idx, base_time + timedelta(days=cid)))
            if idx % 97 == 0:
                # Introduce a duplicate entry to test dedupe logic
                records.append(build_message(cid, idx, base_time + timedelta(days=cid)))
        # Add an intentionally malformed entry for cleaning
        records.append(
            {
                "conversation_id": f"conv-{cid:04d}",
                "message_index": -1,
                "role": "user",
                "content": "",
                "created_at": "not-a-date",
            }
        )
    # Add a couple of entries with US style date format and bytes content
    records.append(
        {
            "conversation_id": "conv-9999",
            "message_index": 0,
            "role": "user",
            "content": "Coffee chat about team culture".encode("utf-8"),
            "created_at": (base_time + timedelta(days=1)).strftime("%m/%d/%Y %H:%M:%S"),
            "metadata": {"source": "imported-csv"},
        }
    )
    records.append(
        {
            "conversation_id": "conv-9999",
            "message_index": 1,
            "role": "assistant",
            "content": "Reply about values & focus areas",
            "created_at": (base_time + timedelta(days=1, minutes=30)).strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
        }
    )

    def coerce_bytes(value: dict) -> dict:
        copy = dict(value)
        content = copy.get("content")
        if isinstance(content, (bytes, bytearray)):
            copy["content"] = content.decode("utf-8", errors="replace")
        return copy

    with OUTPUT_PATH.open("w", encoding="utf-8") as f:
        for record in records:
            json.dump(coerce_bytes(record), f, ensure_ascii=False)
            f.write("\n")

    size_mb = OUTPUT_PATH.stat().st_size / (1024 * 1024)
    print(f"Wrote {len(records)} records to {OUTPUT_PATH} (~{size_mb:.2f} MB)")


if __name__ == "__main__":
    main()
