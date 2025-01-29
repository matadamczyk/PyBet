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

IGNORED_DIRECTORIES = [
    "node_modules",
    "dist",
    "build",
    ".git",
    "venv",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".next",
    ".nuxt",
    "coverage",
    ".coverage",
    ".env",
    "migrations",
]


def format_with_prettier(file_path, check=False):
    """Formats JavaScript, TypeScript, Vue, JSON, HTML, CSS files with Prettier."""
    command = ["npx", "prettier", "--check" if check else "--write", file_path]
    try:
        subprocess.run(command, check=True)
        print(f"{'Checked' if check else 'Formatted'}: {file_path} (Prettier)")
    except subprocess.CalledProcessError as e:
        print(
            f"Error {'checking' if check else 'formatting'} {file_path} with Prettier: {e}"
        )


def format_with_black(file_path, check=False):
    """Formats Python files with Black."""
    command = ["pipx", "run", "black"] + (
        ["--check", file_path] if check else [file_path]
    )
    try:
        subprocess.run(command, check=True)
        print(f"{'Checked' if check else 'Formatted'}: {file_path} (Black)")
    except subprocess.CalledProcessError as e:
        print(
            f"Error {'checking' if check else 'formatting'} {file_path} with Black: {e}"
        )


def is_ignored(file_path):
    """Checks if a file is inside an ignored directory."""
    return any(ignored_dir in str(file_path) for ignored_dir in IGNORED_DIRECTORIES)


def main():
    if len(sys.argv) < 2:
        print("Usage: format-cli <extensions>... [--check]")
        print(f"Supported extensions: {', '.join(SUPPORTED_FORMATS.keys())}")
        sys.exit(1)

    check = "--check" in sys.argv
    extensions = [arg for arg in sys.argv[1:] if arg != "--check"]

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

        print(
            f"Found {len(files_to_format)} .{extension} files to {'check' if check else 'format'}."
        )

        for file_path in files_to_format:
            if SUPPORTED_FORMATS[extension] == "Prettier":
                format_with_prettier(str(file_path), check)
            elif SUPPORTED_FORMATS[extension] == "Black":
                format_with_black(str(file_path), check)


if __name__ == "__main__":
    main()
