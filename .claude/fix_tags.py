#!/usr/bin/env python3
"""Remove duplicate ## Tags sections from body (tags are now in frontmatter)."""
import re
from pathlib import Path

VAULT_ROOT = Path("/Users/hoank/Documents/Study/Knowledge/1 - Go")

def clean_tags_section(filepath):
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    original = content

    # Remove entire ## Tags section (header + all tag lines + trailing newlines)
    # Match: ## Tags\n followed by lines of #tag or blank, until non-tag/blank or end
    pattern = r'\n## Tags\s*\n((?:[ \t]*#[^\n]*\n?)*)'
    content = re.sub(pattern, '\n', content)

    # Also remove trailing bare tag lines at very end of file
    # e.g. lines that are just #tag at end of file
    content = re.sub(r'\n#[a-z\-]+(?:\s+#[a-z\-]+)*\s*$', '', content.strip())
    content = content.rstrip() + '\n'

    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return True
    return False

for md_file in VAULT_ROOT.rglob("*.md"):
    changed = clean_tags_section(md_file)
    if changed:
        print(f"CLEANED: {md_file.relative_to(VAULT_ROOT)}")
    else:
        print(f"OK:      {md_file.relative_to(VAULT_ROOT)}")
