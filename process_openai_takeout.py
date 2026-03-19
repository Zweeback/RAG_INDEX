import json
import os
import datetime

def process_chatgpt_export(json_path, output_dir):
    """
    Liest die 'conversations.json' aus dem OpenAI Takeout und erstellt
    für jeden Chat eine saubere Markdown-Datei, die perfekt für RAG,
    NotebookLM oder Google Pinpoint geeignet ist.
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            conversations = json.load(f)
    except FileNotFoundError:
        print(f"FEHLER: Datei {json_path} nicht gefunden.")
        return

    processed_count = 0
    for conv in conversations:
        title = conv.get('title', 'Untitled')
        if not title:
            title = 'Untitled'

        create_time = datetime.datetime.fromtimestamp(conv.get('create_time', 0)).strftime('%Y-%m-%d')

        # Sicheren Dateinamen erstellen
        safe_title = "".join([c for c in title if c.isalnum() or c in [' ', '-', '_']]).strip()
        filename = f"{create_time}_{safe_title[:50]}.md"
        filepath = os.path.join(output_dir, filename)

        with open(filepath, 'w', encoding='utf-8') as out_f:
            out_f.write(f"# {title}\n\n")
            out_f.write(f"**Datum:** {create_time}\n\n")

            mapping = conv.get('mapping', {})
            for node_id, node in mapping.items():
                if node and 'message' in node and node['message']:
                    msg = node['message']
                    author = msg.get('author', {}).get('role', 'unknown')

                    if author in ['user', 'assistant']:
                        parts = msg.get('content', {}).get('parts', [''])
                        # Es kann vorkommen, dass Teile keine Strings sind (z.B. bei Bildern)
                        content = "".join([p for p in parts if isinstance(p, str)])

                        if content.strip():
                            role_name = "Benny (User)" if author == 'user' else "Alice (Assistant)"
                            out_f.write(f"### {role_name}\n")
                            out_f.write(f"{content}\n\n")

        processed_count += 1

    print(f"ERFOLG: {processed_count} ChatGPT-Konversationen wurden erfolgreich nach '{output_dir}' als Markdown exportiert.")
    print("Diese Dateien können nun in Google NotebookLM, Pinpoint oder ChromaDB hochgeladen werden.")

if __name__ == "__main__":
    # Pfad zur Datei conversations.json (muss im selben Ordner liegen oder Pfad anpassen)
    input_file = "conversations.json"
    output_directory = "Cleaned_Chats_For_Alice"

    print("Starte Extraktion der ChatGPT-Daten...")
    process_chatgpt_export(input_file, output_directory)
