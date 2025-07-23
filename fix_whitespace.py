#!/usr/bin/env python3
"""
Script to fix whitespace issues in Python files:
- W293: blank line contains whitespace
- W291: trailing whitespace
"""

import os
import re
from pathlib import Path


def fix_whitespace_in_file(filepath):
    """Fix whitespace issues in a single file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return 0, 0

    original_lines = lines.copy()
    w293_count = 0
    w291_count = 0

    for i, line in enumerate(lines):
        # Check for W293: blank line contains whitespace
        if line.strip() == '' and len(line) > 1:  # More than just newline
            w293_count += 1
            lines[i] = '\n' if line.endswith('\n') else ''

        # Check for W291: trailing whitespace (non-blank lines)
        elif line.rstrip() != line.rstrip('\n').rstrip('\r\n'):
            w291_count += 1
            # Preserve the original line ending
            if line.endswith('\r\n'):
                lines[i] = line.rstrip() + '\r\n'
            elif line.endswith('\n'):
                lines[i] = line.rstrip() + '\n'
            else:
                lines[i] = line.rstrip()

    # Only write if changes were made
    if lines != original_lines:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(lines)
        except Exception as e:
            print(f"Error writing {filepath}: {e}")
            return 0, 0

    return w293_count, w291_count


def find_python_files(root_dir):
    """Find all Python files in the directory tree."""
    python_files = []
    for root, dirs, files in os.walk(root_dir):
        # Skip hidden directories and common non-source directories
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['__pycache__', 'venv', 'env', 'build', 'dist']]

        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))

    return python_files


def main():
    """Main function to fix whitespace issues."""
    root_dir = '.'
    python_files = find_python_files(root_dir)

    print(f"Found {len(python_files)} Python files")
    print("Fixing whitespace issues...\n")

    total_w293 = 0
    total_w291 = 0
    files_fixed = 0

    for filepath in sorted(python_files):
        w293, w291 = fix_whitespace_in_file(filepath)

        if w293 > 0 or w291 > 0:
            files_fixed += 1
            total_w293 += w293
            total_w291 += w291
            print(f"{filepath}: Fixed W293={w293}, W291={w291}")

    print(f"\nSummary:")
    print(f"Files processed: {len(python_files)}")
    print(f"Files fixed: {files_fixed}")
    print(f"Total W293 (blank line whitespace) fixed: {total_w293}")
    print(f"Total W291 (trailing whitespace) fixed: {total_w291}")
    print(f"Total whitespace issues fixed: {total_w293 + total_w291}")


if __name__ == "__main__":
    main()