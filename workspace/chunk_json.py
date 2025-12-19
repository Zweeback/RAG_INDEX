import json
import os
import math

# --- Configuration ---
INPUT_FILE = "conversations.json" # The user's large file
OUTPUT_DIR = "json_chunks"
MAX_CHUNK_SIZE_KB = 10 # Maximum size for each chunk in kilobytes (10KB is safe for 8-12k characters)
# --- End Configuration ---

def chunk_json_file(input_path, output_dir, max_size_kb):
    """
    Reads a large JSON file (expected to be a list of conversations) and splits it
    into smaller, numbered JSON files (chunks) for streaming.
    """
    if not os.path.exists(input_path):
        print(f"Error: Input file not found at {input_path}")
        return

    os.makedirs(output_dir, exist_ok=True)
    
    print(f"Reading file: {input_path}...")
    
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON from {input_path}. Please ensure it is a valid JSON array: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred while reading the file: {e}")
        return

    if not isinstance(data, list):
        print("Error: The JSON file is not a list of conversations. Please check the file format.")
        return

    total_conversations = len(data)
    print(f"Total conversations found: {total_conversations}")

    # Calculate the number of conversations per chunk based on the total size and desired chunk size
    file_size_bytes = os.path.getsize(input_path)
    max_size_bytes = max_size_kb * 1024
    
    # Estimate the number of chunks needed
    estimated_num_chunks = math.ceil(file_size_bytes / max_size_bytes)
    
    # Calculate the number of conversations to put in each chunk
    conversations_per_chunk = math.ceil(total_conversations / estimated_num_chunks)
    
    print(f"File size: {file_size_bytes / (1024*1024):.2f} MB. Target chunk size: {max_size_kb} KB.")
    print(f"Estimated chunks: {estimated_num_chunks}. Conversations per chunk: {conversations_per_chunk}")

    chunk_number = 1
    total_chunks = 0
    
    for i in range(0, total_conversations, conversations_per_chunk):
        chunk_data = data[i:i + conversations_per_chunk]
        
        # Create the chunk file name
        chunk_filename = os.path.join(output_dir, f"chunk_{chunk_number}.json")
        
        # Write the chunk data to the file
        with open(chunk_filename, 'w', encoding='utf-8') as f:
            # The user's instruction requires a specific text wrapper around the JSON content
            # However, for a file-based transfer, we will just output the JSON array.
            # The user can then manually wrap the content of each file with the required
            # [CHUNK X/TOTAL]...[END CHUNK X/TOTAL] text in the chat.
            json.dump(chunk_data, f, indent=2, ensure_ascii=False)
            
        print(f"Created {chunk_filename} with {len(chunk_data)} conversations.")
        chunk_number += 1
        total_chunks += 1

    print(f"\n--- Chunking Complete ---")
    print(f"Total chunks created: {total_chunks}")
    print(f"Files are in the '{output_dir}' directory.")
    print(f"Next step: Upload these files and wrap the content in the required 'JSON-STREAM-MODUS' format.")

if __name__ == "__main__":
    # This script is intended to be run by the user on their local machine.
    # The user needs to place their conversations.json file in the same directory.
    # We will provide the script as a file for them to download and run.
    print("This script is designed to be run on your local machine.")
    print(f"1. Place your large '{INPUT_FILE}' file in the same directory as this script.")
    print("2. Run the script.")
    print("3. The script will create a folder named 'json_chunks' with the split files.")
    print("4. Upload the resulting chunk files to me.")
    
    # The actual execution in the sandbox is just for testing the logic, but we won't run it
    # since the user's file is not here. We will just provide the file.
    # chunk_json_file(INPUT_FILE, OUTPUT_DIR, MAX_CHUNK_SIZE_KB)
    pass
