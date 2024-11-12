#!/usr/bin/env python3
import subprocess
import sys
import os
from pathlib import Path

SUPPORTED_FORMATS = {
    "js": "Prettier",
    "ts": "Prettier",
    "vue": "Prettier",
    "json": "Prettier",
    "html": "Prettier",
    "css": "Prettier",
    "py": "Black",
}

IGNORED_DIRECTORIES = ['node_modules', 'dist', 'build', '.git']

def format_with_prettier(file_path):
    """Formats JavaScript, TypeScript, Vue, JSON, HTML, CSS files with Prettier."""
    try:
        subprocess.run(["prettier", "--write", file_path], check=True)
        print(f"Formatted: {file_path} (Prettier)")
    except FileNotFoundError:
        print("Prettier is not installed. Install it with: npm install -g prettier")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_path} with Prettier: {e}")

def format_with_black(file_path):
    """Formats Python files with Black."""
    try:
        subprocess.run(["black", file_path], check=True)
        print(f"Formatted: {file_path} (Black)")
    except FileNotFoundError:
        print("Black is not installed. Install it with: pip install black")
    except subprocess.CalledProcessError as e:
        print(f"Error formatting {file_path} with Black: {e}")

def is_ignored(file_path):
    """Checks if a file is inside an ignored directory."""
    return any(ignored_dir in str(file_path) for ignored_dir in IGNORED_DIRECTORIES)

def main():
    if len(sys.argv) < 2:
        print("Usage: format-cli <extensions>...")
        print(f"Supported extensions: {', '.join(SUPPORTED_FORMATS.keys())}")
        sys.exit(1)

    extensions = sys.argv[1:]

    unsupported_extensions = [ext for ext in extensions if ext not in SUPPORTED_FORMATS]
    if unsupported_extensions:
        print(f"Unsupported extensions: {', '.join(unsupported_extensions)}")
        print(f"Supported extensions: {', '.join(SUPPORTED_FORMATS.keys())}")
        sys.exit(1)

    for extension in extensions:
        print(f"Processing files with extension: .{extension}")
        
        files_to_format = list(Path(".").rglob(f"*.{extension}"))
        files_to_format = [file for file in files_to_format if not is_ignored(file)]  

        if not files_to_format:
            print(f"No .{extension} files found in the current directory.")
            continue

        print(f"Found {len(files_to_format)} .{extension} files to format.")

        for file_path in files_to_format:
            if SUPPORTED_FORMATS[extension] == "Prettier":
                format_with_prettier(str(file_path))
            elif SUPPORTED_FORMATS[extension] == "Black":
                format_with_black(str(file_path))

if __name__ == "__main__":
    main()