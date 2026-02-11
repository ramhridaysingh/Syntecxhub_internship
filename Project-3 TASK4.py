          # Project - 3 Folder Backup / Sync Tool

import os
import shutil
import argparse
import logging
from datetime import datetime
import zipfile


# -----------------------------
# Setup Logging
# -----------------------------
def setup_logging():
    logging.basicConfig(
        filename="backup.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )


# -----------------------------
# Create Timestamp Folder
# -----------------------------
def create_backup_folder(destination):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = os.path.join(destination, f"backup_{timestamp}")
    os.makedirs(backup_path, exist_ok=True)
    return backup_path


# -----------------------------
# Copy Files (Incremental)
# -----------------------------
def copy_files(source, backup_path, dry_run=False):
    for root, dirs, files in os.walk(source):
        relative_path = os.path.relpath(root, source)
        dest_dir = os.path.join(backup_path, relative_path)

        if not dry_run:
            os.makedirs(dest_dir, exist_ok=True)

        for file in files:
            src_file = os.path.join(root, file)
            dest_file = os.path.join(dest_dir, file)

            if dry_run:
                print(f"[DRY RUN] Would copy: {src_file}")
                continue

            shutil.copy2(src_file, dest_file)
            logging.info(f"Copied: {src_file}")


# -----------------------------
# Compress Backup Folder
# -----------------------------
def compress_backup(folder_path):
    zip_path = folder_path + ".zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(root, file)
                arcname = os.path.relpath(full_path, folder_path)
                zipf.write(full_path, arcname)

    shutil.rmtree(folder_path)
    logging.info(f"Compressed and removed folder: {folder_path}")
    print(f"Backup compressed to {zip_path}")


# -----------------------------
# Rotate Old Backups
# -----------------------------
def rotate_backups(destination, keep):
    backups = sorted(
        [f for f in os.listdir(destination) if f.startswith("backup_")]
    )

    if len(backups) <= keep:
        return

    old_backups = backups[:-keep]

    for backup in old_backups:
        path = os.path.join(destination, backup)
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        logging.info(f"Deleted old backup: {path}")
        print(f"Deleted old backup: {backup}")


# -----------------------------
# Main
# -----------------------------
def main():
    parser = argparse.ArgumentParser(description="Folder Backup / Sync Tool")

    parser.add_argument("--source", required=True, help="Source folder path")
    parser.add_argument("--destination", required=True, help="Backup destination path")
    parser.add_argument("--dry-run", action="store_true", help="Preview without copying")
    parser.add_argument("--zip", action="store_true", help="Compress backup")
    parser.add_argument("--keep", type=int, default=5, help="Number of backups to keep")

    args = parser.parse_args()

    setup_logging()

    source = args.source
    destination = args.destination

    if not os.path.exists(source):
        print("Source folder does not exist.")
        return

    os.makedirs(destination, exist_ok=True)

    print("Starting backup...")

    backup_folder = create_backup_folder(destination)

    copy_files(source, backup_folder, args.dry_run)

    if not args.dry_run and args.zip:
        compress_backup(backup_folder)

    if not args.dry_run:
        rotate_backups(destination, args.keep)

    print("Backup completed successfully.")


if __name__ == "__main__":
    main()
