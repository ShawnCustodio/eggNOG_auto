#!/usr/bin/env python3
"""
decompress_databases.py
------------------------
Decompresses all .gz database files needed for eggnog_pipeline.py.

Usage:
    python decompress_databases.py
"""

import os
import gzip
import shutil

# ─────────────────────────────────────────────────────────────────────────────
#  EDIT THIS PATH if your folder is somewhere else
# ─────────────────────────────────────────────────────────────────────────────
DB_DIR = r"C:\Users\SKC180002\Downloads\eggNOG\databases"
# ─────────────────────────────────────────────────────────────────────────────

FILES = [
    "e7.proteins.fa",
    "e7.og_info_kegg_go.tsv",
    "e7.protein_families.tsv",
]

def decompress(path: str):
    gz_path = path + ".gz"

    if os.path.exists(path):
        print(f"[SKIP] Already decompressed: {os.path.basename(path)}")
        return

    if not os.path.exists(gz_path):
        print(f"[MISSING] Could not find: {os.path.basename(gz_path)}")
        return

    print(f"[...] Decompressing {os.path.basename(gz_path)} ...")
    with gzip.open(gz_path, "rb") as f_in:
        with open(path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out, length=64 * 1024 * 1024)  # 64MB chunks
    print(f"[DONE] {os.path.basename(path)}")


def main():
    print(f"Database folder: {DB_DIR}\n")
    for filename in FILES:
        decompress(os.path.join(DB_DIR, filename))
    print("\nAll done! You can now run eggnog_pipeline.py")


if __name__ == "__main__":
    main()