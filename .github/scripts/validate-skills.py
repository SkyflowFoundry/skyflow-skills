#!/usr/bin/env python3
"""Validate Skyflow skill directories before packaging.

Each skill under skyflow-skills-plugin/skills/<name>/ must contain a SKILL.md
with YAML frontmatter whose `name` matches the directory and whose
`description` is present. Rules mirror the Agent Skills spec so that every
published zip is a valid, portable skill.

Exit code 0 = all valid, 1 = one or more problems (details printed).
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml

SKILLS_DIR = Path("skyflow-skills-plugin/skills")
FRONTMATTER_RE = re.compile(r"^---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)
NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
NAME_MAX = 64
DESC_MAX = 1024


def parse_frontmatter(text: str) -> dict | None:
    """Parse the leading --- fenced YAML block into a dict.

    Uses a full YAML parser so multi-line values (block scalars, quoted
    strings spanning lines) are handled correctly. Returns None if there is
    no frontmatter block or it is not a YAML mapping.
    """
    m = FRONTMATTER_RE.match(text)
    if not m:
        return None
    try:
        data = yaml.safe_load(m.group(1))
    except yaml.YAMLError:
        return None
    return data if isinstance(data, dict) else None


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    skill_md = skill_dir / "SKILL.md"
    if not skill_md.is_file():
        return [f"{skill_dir.name}: missing SKILL.md"]

    fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
    if fm is None:
        return [f"{skill_dir.name}: SKILL.md has no valid --- YAML frontmatter block"]

    name = fm.get("name")
    if not name or not isinstance(name, str):
        errors.append(f"{skill_dir.name}: frontmatter missing `name`")
    else:
        if name != skill_dir.name:
            errors.append(
                f"{skill_dir.name}: frontmatter name `{name}` does not match directory"
            )
        if len(name) > NAME_MAX:
            errors.append(f"{skill_dir.name}: name exceeds {NAME_MAX} chars")
        if not NAME_RE.match(name):
            errors.append(
                f"{skill_dir.name}: name `{name}` must be lowercase letters, digits, and hyphens"
            )

    desc = fm.get("description")
    if not desc or not isinstance(desc, str) or not desc.strip():
        errors.append(f"{skill_dir.name}: frontmatter missing `description`")
    elif len(desc) > DESC_MAX:
        errors.append(
            f"{skill_dir.name}: description exceeds {DESC_MAX} chars ({len(desc)})"
        )

    return errors


def main() -> int:
    if not SKILLS_DIR.is_dir():
        print(f"error: {SKILLS_DIR} not found (run from repo root)", file=sys.stderr)
        return 1

    skill_dirs = sorted(p for p in SKILLS_DIR.iterdir() if p.is_dir())
    if not skill_dirs:
        print(f"error: no skills found under {SKILLS_DIR}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for skill_dir in skill_dirs:
        errs = validate_skill(skill_dir)
        if errs:
            all_errors.extend(errs)
        else:
            print(f"  ok  {skill_dir.name}")

    if all_errors:
        print("\nValidation failed:", file=sys.stderr)
        for e in all_errors:
            print(f"  - {e}", file=sys.stderr)
        return 1

    print(f"\nAll {len(skill_dirs)} skills valid.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
