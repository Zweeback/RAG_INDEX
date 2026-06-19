# --- Google Drive Inventory & Categorization Script for Colab ---

import os
import shutil
import pandas as pd
from datetime import datetime
from google.colab import drive

# 1. Mount Google Drive
print("Mounting Google Drive...")
drive.mount('/content/drive')

# 2. Configuration
# We will scan the root of Google Drive.
# WARNING: It's recommended to test this on a specific subfolder first!
# Example: ROOT_DIR = '/content/drive/MyDrive/TestFolder'
ROOT_DIR = '/content/drive/MyDrive'

# Dry run mode: If True, the script will only print what it WOULD do, without actually moving files.
# SET TO FALSE ONLY WHEN YOU ARE SURE!
DRY_RUN = True

# Target directory for categorized files
# Files will be moved to /content/drive/MyDrive/Categorized_Cleanup/<Category_Name>
TARGET_DIR = os.path.join(ROOT_DIR, 'Categorized_Cleanup')

# 3. Define Categories based on file extensions
CATEGORIES = {
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp', '.heic'],
    'Documents': ['.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt', '.xls', '.xlsx', '.csv', '.ppt', '.pptx', '.pages', '.numbers', '.key'],
    'Videos': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
    'Audio': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    'Archives': ['.zip', '.rar', '.tar', '.gz', '.7z'],
    'Code_and_Scripts': ['.py', '.html', '.css', '.js', '.json', '.xml', '.c', '.cpp', '.java', '.sh', '.bat'],
    'Others': [] # Files that don't match any category
}

def get_category(file_ext):
    for category, extensions in CATEGORIES.items():
        if file_ext.lower() in extensions:
            return category
    return 'Others'

def inventory_and_categorize():
    file_data = []

    print(f"Scanning directory: {ROOT_DIR}")

    # Create target directories if they don't exist (only if not a dry run)
    if not DRY_RUN:
        if not os.path.exists(TARGET_DIR):
            os.makedirs(TARGET_DIR)
        for category in CATEGORIES.keys():
            cat_path = os.path.join(TARGET_DIR, category)
            if not os.path.exists(cat_path):
                os.makedirs(cat_path)

    moved_count = 0
    error_count = 0

    for root, dirs, files in os.walk(ROOT_DIR):
        # Skip the target directory to avoid infinite loops or moving already moved files
        if TARGET_DIR in root:
            continue

        for file in files:
            file_path = os.path.join(root, file)

            try:
                # Extract metadata
                size_bytes = os.path.getsize(file_path)
                mod_time = os.path.getmtime(file_path)
                mod_time_str = datetime.fromtimestamp(mod_time).strftime('%Y-%m-%d %H:%M:%S')
                _, ext = os.path.splitext(file)

                category = get_category(ext)

                # Append to inventory list
                file_data.append({
                    'Filename': file,
                    'Path': file_path,
                    'Size (Bytes)': size_bytes,
                    'Extension': ext,
                    'Last Modified': mod_time_str,
                    'Category': category
                })

                # Categorization (Moving files)
                dest_dir = os.path.join(TARGET_DIR, category)
                dest_path = os.path.join(dest_dir, file)

                # Avoid moving if the file is already in the right place
                if root != dest_dir:
                    if DRY_RUN:
                        print(f"[DRY RUN] Would move: '{file_path}' -> '{dest_path}'")
                    else:
                        # Handle duplicate filenames
                        if os.path.exists(dest_path):
                            base, extension = os.path.splitext(file)
                            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                            new_name = f"{base}_{timestamp}{extension}"
                            dest_path = os.path.join(dest_dir, new_name)

                        shutil.move(file_path, dest_path)
                        print(f"Moved: '{file}' to '{category}'")
                        moved_count += 1

            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                error_count += 1

    # 4. Generate Inventory CSV
    df = pd.DataFrame(file_data)
    inventory_file = os.path.join(ROOT_DIR, 'GoogleDrive_Inventory.csv')
    df.to_csv(inventory_file, index=False)

    print("\n--- Summary ---")
    print(f"Total files scanned: {len(file_data)}")
    print(f"Inventory saved to: {inventory_file}")

    if DRY_RUN:
        print("\nThis was a DRY RUN. No files were actually moved.")
        print("To actually move files, set DRY_RUN = False in the script and run again.")
    else:
        print(f"Files successfully moved: {moved_count}")
        print(f"Errors encountered: {error_count}")

# Execute the function
if __name__ == "__main__":
    inventory_and_categorize()
