#!/usr/bin/env python3
"""
Cleanup script for Qdrant storage lock files.
Run this if you get "Storage folder is already accessed" errors.
"""

import os
import shutil
import glob

QDRANT_PATH = "./qdrant_storage"

def cleanup_qdrant_locks():
    """Remove Qdrant lock files to fix access issues."""
    print(f"Cleaning up Qdrant storage at: {QDRANT_PATH}")
    
    # Look for lock files
    lock_patterns = [
        os.path.join(QDRANT_PATH, "**", "*.lock"),
        os.path.join(QDRANT_PATH, "**", ".lock"),
        os.path.join(QDRANT_PATH, ".qdrant.lock"),
    ]
    
    removed_count = 0
    for pattern in lock_patterns:
        for lock_file in glob.glob(pattern, recursive=True):
            try:
                os.remove(lock_file)
                print(f"  ✓ Removed: {lock_file}")
                removed_count += 1
            except Exception as e:
                print(f"  ✗ Failed to remove {lock_file}: {e}")
    
    if removed_count == 0:
        print("  No lock files found.")

if __name__ == "__main__":
    cleanup_qdrant_locks()
