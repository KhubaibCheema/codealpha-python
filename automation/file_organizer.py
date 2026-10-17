"""CodeAlpha Task 4 — Task Automation: File Organizer.

Picks up loose files in a folder and sorts them into subfolders by type
(documents, images, audio, archives, other). Run in DRY RUN mode first.

Run:  python file_organizer.py "/path/to/messy/folder" [--dry-run]
      Use --no-dry-run to actually move the files.
"""
import argparse
import shutil
from pathlib import Path

CATEGORIES = {
    "images": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".bmp"},
    "documents": {".pdf", ".docx", ".doc", ".txt", ".md", ".xlsx", ".pptx"},
    "audio": {".mp3", ".wav", ".ogg", ".m4a"},
    "video": {".mp4", ".mkv", ".avi", ".mov"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
}


def categorize(file_path):
    """Return the category name for file_path's suffix, or 'other'."""
    suffix = file_path.suffix.lower()
    for category, extensions in CATEGORIES.items():
        if suffix in extensions:
            return category
    return "other"


def organize(folder, dry_run=True):
    """Sort files directly inside folder into category subfolders."""
    folder = Path(folder)
    if not folder.is_dir():
        print(f"Error: '{folder}' is not a valid folder.")
        return

    counts = {}
    for item in folder.iterdir():
        if not item.is_file():
            continue  # skip subfolders
        category = categorize(item)
        target_dir = folder / category
        counts[category] = counts.get(category, 0) + 1

        if dry_run:
            print(f"[DRY RUN] would move '{item.name}' -> '{category}/'")
        else:
            target_dir.mkdir(exist_ok=True)
            shutil.move(str(item), str(target_dir / item.name))
            print(f"moved '{item.name}' -> '{category}/'")

    print("\n--- Summary ---")
    if not counts:
        print("No files found to organize.")
    for category in sorted(counts):
        action = "would move" if dry_run else "moved"
        print(f"{category}: {counts[category]} file(s) {action}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Organize a messy folder by file type.")
    parser.add_argument("folder", help="folder to organize")
    parser.add_argument("--dry-run", action=argparse.BooleanOptionalAction,
                        default=True,
                        help="preview only (default); use --no-dry-run to move files")
    args = parser.parse_args()
    organize(Path(args.folder), dry_run=args.dry_run)
