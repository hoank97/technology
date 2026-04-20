#!/usr/bin/env python3
"""
Fix frontmatter for ALL modules (1-6) in Knowledge vault.
Handles various file formats:
- parent:: inside YAML block
- parent:: outside YAML but body has ## Tags
- Missing type/status/date_created/tags
- No YAML frontmatter at all
"""
import re
from pathlib import Path

VAULT = Path("/Users/hoank/Documents/Study/Knowledge")

# Module-level index files (no date_created needed, simpler metadata)
INDEX_MODULES = {
    "2 - CS Fundamentals/2 - CS Fundamentals.md",
    "3 - Infrastructure/3 - Infrastructure.md",
    "4 - Networking/4 - Networking.md",
    "5 - Ecosystem/5 - Ecosystem.md",
    "6 - System Design/6 - System Design.md",
    "2 - CS Fundamentals/2.5 - DSA.md",
    "2 - CS Fundamentals/DSA Patterns/00 - DSA Patterns.md",
    "1 - Go/1 - Go.md",
}

# For sub-folder index files
SUBINDEX_MODULES = {
    "1 - Go/01 - Language Basics/01 - Language Basics.md",
    "1 - Go/02 - Memory & Runtime/02 - Memory & Runtime.md",
    "1 - Go/03 - Concurrency/03 - Concurrency.md",
    "1 - Go/04 - Error Handling/04 - Error Handling.md",
    "1 - Go/05 - Generics/05 - Generics.md",
    "1 - Go/06 - Standard Library/06 - Standard Library.md",
    "1 - Go/07 - Testing & Tooling/07 - Testing & Tooling.md",
}

# Module name → tags for index files
INDEX_TAGS = {
    "2 - CS Fundamentals": ["cs", "fundamentals"],
    "3 - Infrastructure": ["infrastructure", "security", "cryptography"],
    "4 - Networking": ["networking", "socket", "http", "grpc"],
    "5 - Ecosystem": ["ecosystem", "docker", "git", "ai"],
    "6 - System Design": ["system-design", "database", "architecture"],
    "2.5 - DSA": ["dsa", "algorithms", "interview"],
    "00 - DSA Patterns": ["dsa", "patterns", "algorithms"],
}


def get_type_from_path(filepath):
    """Determine file type from path."""
    name = filepath.name
    if any(ind in str(filepath) for ind in INDEX_MODULES):
        return "index"
    if any(ind in str(filepath) for ind in SUBINDEX_MODULES):
        return "index"
    # DSA pattern files are reference/concept
    if "DSA Patterns" in str(filepath):
        if "00 -" in name:
            return "index"
        return "concept"
    # Content files
    if name.startswith(("0", "1", "2", "3", "4", "5", "6")):
        parts = name.split(" ")
        if len(parts) > 0 and parts[0].endswith(" -"):
            return "index"
        # Has chapter number like "2.1", "3.2"
        if re.match(r"^\d+\.\d+", parts[0]):
            return "concept"
    return "concept"


def extract_tags_from_body(content):
    """Extract tags from ## Tags section in body."""
    match = re.search(r'^## Tags\s*\n((?:[ \t]*#[a-z0-9\-]+\s*)*)', content, re.MULTILINE)
    if match:
        tag_line = match.group(1)
        tags = [t.strip().lstrip('#') for t in tag_line.split() if t.strip()]
        return tags
    return []


def remove_tags_section(content):
    """Remove ## Tags section from body."""
    content = re.sub(r'\n## Tags\s*\n((?:[ \t]*#[a-z0-9\-]+\s*)*)', '\n', content)
    # Also remove trailing bare tags at end
    content = re.sub(r'\n(#[a-z0-9\-]+(?:\s+#[a-z0-9\-]+)*)\s*$', '\n', content)
    return content


def fix_file(filepath):
    """Fix a single file's frontmatter."""
    with open(filepath, encoding="utf-8") as f:
        content = f.read()

    original = content

    # --- Step 1: Extract parent:: and children:: from body ---
    parent_line = None
    children_lines = []

    # Find parent:: in body
    parent_match = re.search(r'\nparent:: \[\[([^\]]+)\]\]', content)
    if parent_match:
        parent_line = f"parent:: [[{parent_match.group(1)}]]"
        content = content[:parent_match.start()] + content[parent_match.end():]

    # Find all children:: in body
    for child_match in reversed(list(re.finditer(r'\nchildren:: \[\[([^\]]+)\]\]', content))):
        children_lines.insert(0, f"children:: [[{child_match.group(1)}]]")
        content = content[:child_match.start()] + content[child_match.end():]

    # --- Step 2: Extract tags from body ---
    body_tags = extract_tags_from_body(content)
    content = remove_tags_section(content)

    # --- Step 3: Parse and clean YAML block ---
    lines = content.split('\n')
    new_lines = []
    in_yaml = False
    yaml_fields = {}
    parent_in_yaml = None
    children_in_yaml = []

    for line in lines:
        stripped = line.strip()
        if stripped == '---':
            if not in_yaml:
                in_yaml = True
                new_lines.append(line)
            else:
                new_lines.append(line)
                in_yaml = False
        elif in_yaml:
            if stripped.startswith('parent::'):
                parent_in_yaml = stripped
            elif stripped.startswith('children::'):
                children_in_yaml.append(stripped)
            elif ':' in stripped:
                key = stripped.split(':')[0].strip()
                yaml_fields[key] = stripped
            # Skip inline fields - don't add to new_lines
        else:
            new_lines.append(line)

    content = '\n'.join(new_lines)

    # --- Step 4: Determine file metadata ---
    is_index = get_type_from_path(filepath) == "index"
    file_type = "index" if is_index else "concept"
    date_created = "date_created: 2026-04-21" if not is_index else ""

    # --- Step 5: Determine tags ---
    # Infer module tags
    rel = str(filepath.relative_to(VAULT))
    module_tags = []
    for mod_name, tags in INDEX_TAGS.items():
        if mod_name in rel:
            module_tags = tags
            break
    if not module_tags:
        module_tags = ["concept"]  # fallback

    all_tags = sorted(set(module_tags + body_tags))
    tags_line = f"tags: [{', '.join(all_tags)}]" if all_tags else None

    # --- Step 6: Build new YAML block ---
    yaml = ["---"]
    yaml.append(f"type: {file_type}")
    yaml.append("status: complete")
    if date_created:
        yaml.append(date_created)
    if tags_line:
        yaml.append(tags_line)
    yaml.append("---")

    # --- Step 7: Reconstruct file ---
    # Find the YAML block boundary
    parts = content.split('\n---\n', 1)
    if len(parts) == 2:
        yaml_content, body = parts
        # Re-add parent/children after YAML block
        after_yaml = []
        if parent_in_yaml:
            after_yaml.append(parent_in_yaml)
        for cl in children_in_yaml:
            after_yaml.append(cl)
        if parent_line:
            after_yaml.insert(0, parent_line)
        after_yaml.extend(children_lines)

        result = '\n'.join(yaml) + '\n'
        if after_yaml:
            result += '\n'.join(after_yaml) + '\n'
        result += '\n' + body
    else:
        # No YAML block found - add one at the start
        after_yaml = []
        if parent_line:
            after_yaml.append(parent_line)
        after_yaml.extend(children_lines)
        result = '\n'.join(yaml) + '\n'
        if after_yaml:
            result += '\n'.join(after_yaml) + '\n'
        result += content

    # Clean up extra blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)
    result = result.strip() + '\n'

    if result != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(result)
        return True
    return False


def main():
    fixed = 0
    errors = []

    # Process all .md files except .claude and "1 - Go"
    for md in sorted(VAULT.rglob("*.md")):
        rel = str(md.relative_to(VAULT))
        # Skip .claude and 1 - Go (already fixed)
        if ".claude" in rel or rel.startswith("1 - Go"):
            continue
        # Skip README and root index
        if md.name in ("README.md", "CLAUDE.md"):
            continue

        try:
            changed = fix_file(md)
            status = "MODIFIED" if changed else "unchanged"
            print(f"  [{status}] {rel}")
            fixed += 1
        except Exception as e:
            errors.append((rel, str(e)))
            print(f"  [ERROR] {rel}: {e}")

    print(f"\nProcessed {fixed} files")
    if errors:
        print(f"\nErrors ({len(errors)}):")
        for path, err in errors:
            print(f"  ERROR: {path} — {err}")


if __name__ == "__main__":
    main()