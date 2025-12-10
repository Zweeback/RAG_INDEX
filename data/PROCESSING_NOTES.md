# ChatGPT Export Cleaning Notes

## Stichprobe und Struktur
- Quelle: `data/raw/chat_export_sample.jsonl` (~0.9 MB, 3,692 Zeilen)
- Erfasste Keys in der Rohdatei: `conversation_id`, `message_index`, `role`, `content`, `created_at`, `metadata`
- Beispiele für Inhalte: Rollen `user`, `assistant`, `system`; Zeitstempel in ISO-Format sowie US-Datumsformaten; `metadata` mit Modellen, Sprache und Tags.

## Pflicht- und optionale Felder
- **Pflichtfelder:** `conversation_id`, `message_index`, `role`, `content`, `created_at`
- **Optionale Felder:** `metadata` (inkl. `model`, `language`, `tags`, `parent_id`, `custom_note`), `source`, weitere frei bestimmbare Schlüssel

## Bereinigungsregeln
- **Duplikate entfernen:** gleiche Kombination aus `conversation_id` + `message_index` + `role` wird nur einmal behalten.
- **Leere/defekte Einträge verwerfen:** Records ohne Pflichtfelder, ohne Inhalt, mit unbekannter Rolle oder ohne parsbaren Zeitstempel werden entfernt.
- **Datumsnormalisierung:** verschiedene Formate werden in UTC ISO-8601 überführt (Beibehaltung von Sekunden/Millisekunden; fehlende Zeitzone → UTC angenommen).
- **Charset-Normalisierung:** sämtliche Textfelder werden als UTF-8 interpretiert, nicht-dekodierbare Zeichen werden ersetzt.

## Artefakte
- **Gereinigter Export:** `data/processed/cleaned_messages.jsonl` (3,602 Records)
- **Goldene Validierungsprobe:** `data/validation/golden_sample.jsonl` (erste 50 bereinigte Records, stabil zur Regressionsprüfung)

## Nutzung
Führe `python scripts/process_chat_export.py` aus, um die Rohstichprobe zu validieren, zu bereinigen und die goldene Probe neu zu erstellen.
