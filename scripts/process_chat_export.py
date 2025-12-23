"""Clean and normalize ChatGPT export samples for RAG ingestion."""
from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List

RAW_SAMPLE = Path("data/raw/chat_export_sample.jsonl")
CLEANED_PATH = Path("data/processed/cleaned_messages.jsonl")
GOLDEN_SAMPLE = Path("data/validation/golden_sample.jsonl")

MANDATORY_FIELDS = ["conversation_id", "message_index", "role", "content", "created_at"]
OPTIONAL_FIELDS = ["metadata", "model", "language", "tags", "parent_id", "custom_note"]
DUPLICATE_KEY = ("conversation_id", "message_index", "role")

DATE_PATTERNS = [
    "%Y-%m-%dT%H:%M:%S.%f%z",
    "%Y-%m-%dT%H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S%z",
    "%Y-%m-%d %H:%M:%S",
    "%m/%d/%Y %H:%M:%S",
]


def load_sample(path: Path, max_bytes: int = 5 * 1024 * 1024) -> List[Dict]:
    if not path.exists():
        raise FileNotFoundError(f"Missing sample file at {path}")
    records: List[Dict] = []
    consumed = 0
    with path.open("rb") as f:
        for raw_line in f:
            consumed += len(raw_line)
            if consumed > max_bytes:
                break
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue
            records.append(json.loads(line))
    return records


def normalize_text(value) -> str:
    if value is None:
        return ""
    if isinstance(value, (bytes, bytearray)):
        value = value.decode("utf-8", errors="replace")
    return str(value).encode("utf-8", errors="replace").decode("utf-8")


def normalize_created_at(value: str) -> str | None:
    if not value:
        return None
    candidate = str(value).strip()
    for pattern in DATE_PATTERNS:
        try:
            dt = datetime.strptime(candidate, pattern)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt.astimezone(timezone.utc).isoformat()
        except ValueError:
            continue
    try:
        dt = datetime.fromisoformat(candidate)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(timezone.utc).isoformat()
    except ValueError:
        return None


def normalize_record(record: Dict) -> Dict | None:
    normalized: Dict = {}
    for field in MANDATORY_FIELDS:
        normalized[field] = record.get(field)
    normalized["content"] = normalize_text(normalized.get("content"))
    normalized["role"] = normalize_text(normalized.get("role")).strip().lower()
    normalized["conversation_id"] = normalize_text(normalized.get("conversation_id")).strip()
    normalized["message_index"] = record.get("message_index")
    normalized_date = normalize_created_at(record.get("created_at"))
    normalized["created_at"] = normalized_date

    metadata = record.get("metadata") or {}
    if not isinstance(metadata, dict):
        metadata = {}
    normalized["metadata"] = metadata

    if not normalized["conversation_id"] or normalized["message_index"] is None:
        return None
    if normalized["role"] not in {"user", "assistant", "system"}:
        return None
    if not normalized["content"].strip():
        return None
    if normalized_date is None:
        return None

    return normalized


def deduplicate(records: Iterable[Dict]) -> List[Dict]:
    seen = set()
    unique: List[Dict] = []
    for record in records:
        key = tuple(record.get(field) for field in DUPLICATE_KEY)
        if key in seen:
            continue
        seen.add(key)
        unique.append(record)
    return unique


def write_jsonl(path: Path, records: Iterable[Dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for record in records:
            json.dump(record, f, ensure_ascii=False)
            f.write("\n")


def inspect_structure(records: List[Dict]) -> Dict[str, int]:
    key_counter: Counter = Counter()
    for record in records:
        for key in record.keys():
            key_counter[key] += 1
    return dict(key_counter)


def build_golden_sample(records: List[Dict], size: int = 50) -> List[Dict]:
    return records[:size]


def main() -> None:
    raw_records = load_sample(RAW_SAMPLE)
    print(f"Loaded {len(raw_records)} raw records from {RAW_SAMPLE}")
    structure_counts = inspect_structure(raw_records)
    print("Observed keys (with frequency):")
    for key, count in sorted(structure_counts.items()):
        print(f"  - {key}: {count}")

    normalized = [rec for rec in (normalize_record(r) for r in raw_records) if rec]
    print(f"After normalization: {len(normalized)} records remain")

    deduped = deduplicate(normalized)
    print(f"After deduplication: {len(deduped)} records remain")

    write_jsonl(CLEANED_PATH, deduped)
    print(f"Wrote cleaned dataset to {CLEANED_PATH}")

    golden = build_golden_sample(deduped)
    write_jsonl(GOLDEN_SAMPLE, golden)
    print(f"Saved golden sample ({len(golden)} records) to {GOLDEN_SAMPLE}")


if __name__ == "__main__":
    main()
