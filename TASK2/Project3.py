                          #Project 3: File Organizer Script

import os
import shutil
from datetime import datetime


LOG_FILE = "file_organizer.log"


def log_message(message):
    with open(LOG_FILE, "a") as log:
        log.write(message + "\n")


def get_unique_name(folder, filename):
    name, ext = os.path.splitext(filename)
    counter = 1

    new_name = filename
    while os.path.exists(os.path.join(folder, new_name)):
        new_name = f"{name}_{counter}{ext}"
        counter += 1

    return new_name


def organize_files(path, dry_run=False):
    if not os.path.exists(path):
        print("❌ Folder does not exist.")
        return

    files = os.listdir(path)

    for file in files:
        file_path = os.path.join(path, file)

        if os.path.isfile(file_path):
            ext = os.path.splitext(file)[1].lower()

            if ext == "":
                folder_name = "No_Extension"
            else:
                folder_name = ext[1:].upper() + "_Files"

            target_folder = os.path.join(path, folder_name)

            if not os.path.exists(target_folder):
                if not dry_run:
                    os.makedirs(target_folder)

            new_name = get_unique_name(target_folder, file)
            target_path = os.path.join(target_folder, new_name)

            if dry_run:
                print(f"[DRY RUN] {file} → {folder_name}/")
            else:
                shutil.move(file_path, target_path)
                log_message(f"{datetime.now()} : Moved {file} → {folder_name}/")
                print(f"Moved: {file} → {folder_name}/")

# main execution

def main():
    print("📂 File Organizer Script")
    folder_path = input("Enter folder path to organize: ")

    choice = input("Enable dry run? (yes/no): ").lower()
    dry_run = True if choice == "yes" else False

    organize_files(folder_path, dry_run)

    if dry_run:
        print("\n✅ Dry run completed. No files were moved.")
    else:
        print("\n✅ Files organized successfully.")


main()
