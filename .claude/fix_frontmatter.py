#!/usr/bin/env python3
"""
Fix Obsidian frontmatter issues for Knowledge vault.

Issue #1: Move parent::/children:: outside YAML block
Issue #2: Extract tags from body and add to YAML frontmatter
Issue #3: Add type, status, date_created to YAML frontmatter

Usage: python3 fix_frontmatter.py
"""

import re
import os
from pathlib import Path

VAULT_ROOT = Path("/Users/hoank/Documents/Study/Knowledge")

# File metadata: (relative_path, type, existing_tags)
# Tags extracted from existing body sections
FILE_METADATA = {
    "1 - Go/1 - Go.md":                        {"type": "index", "tags": ["go", "module"]},
    "01 - Language Basics/01 - Language Basics.md": {"type": "index", "tags": []},
    "01 - Language Basics/01.1 - Data Types & Basics.md": {"type": "concept", "tags": ["go", "data-types", "slice", "map", "interface", "escape-analysis"]},
    "01 - Language Basics/01.2 - Control Flow & Functions.md": {"type": "concept", "tags": ["go", "control-flow", "function", "closure", "defer"]},
    "02 - Memory & Runtime/02 - Memory & Runtime.md": {"type": "index", "tags": []},
    "02 - Memory & Runtime/02.1 - Memory & Runtime.md": {"type": "concept", "tags": ["go", "memory", "stack", "heap", "gc", "escape-analysis", "sync-pool"]},
    "02 - Memory & Runtime/02.2 - Memory Model.md": {"type": "concept", "tags": ["go", "memory-model", "happens-before", "race", "sync"]},
    "03 - Concurrency/03 - Concurrency.md":         {"type": "index", "tags": []},
    "03 - Concurrency/03.1 - Goroutine & Scheduler.md": {"type": "concept", "tags": ["go", "goroutine", "gmp", "scheduler", "gopark", "context-switch"]},
    "03 - Concurrency/03.2 - Channel & Select.md":  {"type": "concept", "tags": ["go", "channel", "select", "unbuffered", "buffered", "nil-channel", "close"]},
    "03 - Concurrency/03.3 - Concurrency Tools.md": {"type": "concept", "tags": ["go", "sync", "mutex", "rwmutex", "once", "pool", "errgroup", "context"]},
    "04 - Error Handling/04 - Error Handling.md":   {"type": "index", "tags": []},
    "04 - Error Handling/04.1 - Error is a Value.md": {"type": "concept", "tags": ["go", "error", "sentinel-error", "error-handling"]},
    "04 - Error Handling/04.2 - Custom Error.md":   {"type": "concept", "tags": ["go", "error", "custom-error", "wrap", "fmt-errorf"]},
    "04 - Error Handling/04.3 - Panic & Recover.md": {"type": "concept", "tags": ["go", "panic", "recover", "defer", "runtime-goexit"]},
    "05 - Generics/05 - Generics.md":              {"type": "index", "tags": []},
    "05 - Generics/05.1 - Generics.md":            {"type": "concept", "tags": ["go", "generics", "type-parameter", "constraint", "gcshape"]},
    "05 - Generics/05.2 - Generic Algorithms (std).md": {"type": "reference", "tags": ["go", "generics", "slices", "maps", "constraints"]},
    "06 - Standard Library/06 - Standard Library.md": {"type": "index", "tags": []},
    "06 - Standard Library/06.1 - Structured Logging (slog).md": {"type": "concept", "tags": ["go", "slog", "logging", "log-level", "json-handler", "text-handler"]},
    "07 - Testing & Tooling/07 - Testing & Tooling.md": {"type": "index", "tags": []},
    "07 - Testing & Tooling/07.1 - Testing.md":    {"type": "concept", "tags": ["go", "testing", "benchmark", "fuzz", "stub", "mock"]},
    "07 - Testing & Tooling/07.2 - Build & Tooling.md": {"type": "reference", "tags": ["go", "build", "tooling", "pprof", "trace", "gofmt", "go vet", "cover"]},
}


def extract_tags_from_body(content):
    """Extract tags from ## Tags section in body."""
    match = re.search(r'^## Tags\s*\n((?:#\w+\s*)+)', content, re.MULTILINE)
    if match:
        tag_line = match.group(1)
        tags = [t.strip().lstrip('#') for t in tag_line.split() if t.strip()]
        return tags
    return []


def remove_tags_section(content):
    """Remove ## Tags section from body."""
    # Remove the entire ## Tags section (header + content + trailing newlines)
    pattern = r'\n## Tags\s*\n((?:#[\w#\s]+\n?)*)'
    return re.sub(pattern, '', content)


def fix_file(filepath):
    """Fix a single file's frontmatter."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    original = content

    # Pattern: YAML block followed by parent::/children:: and closing ---
    # Current pattern:
    # ---
    #
    # parent:: [[...]]
    # children:: [[...]]
    #
    # ---
    yaml_block_pattern = re.compile(
        r'^(---\n)(\s*)(parent::[^\n]*\n)((\s*)(children::[^\n]*\n)*)',
        re.MULTILINE
    )

    has_inline_fields = yaml_block_pattern.search(content)

    # Extract inline fields from YAML block if present
    parent_line = None
    children_lines = []

    if has_inline_fields:
        parent_line = has_inline_fields.group(3).strip()
        all_inline = has_inline_fields.group(1) + has_inline_fields.group(3) + has_inline_fields.group(4)
        content = content.replace(all_inline, '')

    # Also check if parent/children are still in the YAML (after first removal attempt)
    # The pattern above handles it, but let's do a second pass for safety
    yaml_end_pattern = re.compile(r'^---\s*$', re.MULTILINE)
    lines = content.split('\n')
    new_lines = []
    parent_line = None
    children_lines = []
    in_yaml = False
    yaml_fields = []

    for line in lines:
        if line.strip() == '---':
            if not in_yaml:
                in_yaml = True
                new_lines.append(line)
            else:
                # End of YAML block
                new_lines.append(line)
                in_yaml = False
        elif in_yaml and (line.strip().startswith('parent::') or line.strip().startswith('children::')):
            # This is an inline field INSIDE YAML block - extract it
            if line.strip().startswith('parent::'):
                parent_line = line.strip()
            else:
                children_lines.append(line.strip())
            # Don't add to new_lines (skip it)
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)

    # Extract tags from body
    body_tags = extract_tags_from_body(content)
    content = remove_tags_section(content)

    # Get file metadata
    rel_path = str(filepath.relative_to(VAULT_ROOT / "1 - Go"))
    meta = FILE_METADATA.get(rel_path, {"type": "concept", "tags": []})

    all_tags = sorted(set(meta["tags"] + body_tags))

    # Build new YAML frontmatter
    yaml_lines = ["---"]
    yaml_lines.append("type: " + meta["type"])
    yaml_lines.append("status: complete")
    yaml_lines.append("date_created: 2026-04-21")
    if all_tags:
        yaml_lines.append("tags: [" + ", ".join(all_tags) + "]")
    yaml_lines.append("---")

    # Find where to split content (after the YAML block's closing ---)
    # Pattern: the closing --- of the YAML block (which may have been cleaned)
    parts = content.split('\n---\n', 1)
    if len(parts) == 2:
        yaml_and_close, rest = parts
        # Check if yaml block has already been cleaned (no parent/children inside)
        new_yaml = '\n'.join(yaml_lines)
        content = new_yaml + "\n\n"
        if parent_line:
            content += parent_line + "\n"
        for cl in children_lines:
            content += cl + "\n"
        content += "\n" + rest
    else:
        # Fallback: prepend new YAML
        content = '\n'.join(yaml_lines) + "\n\n" + content

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False


def main():
    go_dir = VAULT_ROOT / "1 - Go"
    fixed = []
    errors = []

    for rel_path in FILE_METADATA:
        filepath = go_dir / rel_path
        if filepath.exists():
            try:
                changed = fix_file(filepath)
                fixed.append((rel_path, changed))
            except Exception as e:
                errors.append((rel_path, str(e)))
        else:
            errors.append((rel_path, "FILE NOT FOUND"))

    print(f"Processed {len(fixed)} files")
    for path, changed in fixed:
        status = "MODIFIED" if changed else "unchanged"
        print(f"  [{status}] {path}")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for path, err in errors:
            print(f"  ERROR: {path} — {err}")


if __name__ == "__main__":
    main()