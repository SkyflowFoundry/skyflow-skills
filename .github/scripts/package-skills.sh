#!/usr/bin/env bash
#
# Package each Skyflow skill directory into a portable zip.
#
# Each zip extracts to <skill-name>/SKILL.md so it can be dropped straight into
# ~/.claude/skills/ (or a project's .claude/skills/) or handed to any harness
# that understands the Agent Skills format. Repo-only cruft is excluded so the
# artifact is clean.
#
# Output: dist/<skill-name>.zip for every skill, plus dist/SHA256SUMS.txt.
set -euo pipefail

SKILLS_DIR="skyflow-skills-plugin/skills"
OUT_DIR="dist"

# Files that exist for repo/contributor purposes and don't belong in a
# portable, runtime-facing skill artifact.
EXCLUDES=(
  '*/.DS_Store'
  '*/CONTRIBUTING.md'
  '*.tmp'
  '*.log'
)

if [[ ! -d "$SKILLS_DIR" ]]; then
  echo "error: $SKILLS_DIR not found (run from repo root)" >&2
  exit 1
fi

rm -rf "$OUT_DIR"
mkdir -p "$OUT_DIR"
OUT_ABS="$(cd "$OUT_DIR" && pwd)"

shopt -s nullglob
count=0
for skill_path in "$SKILLS_DIR"/*/; do
  skill="$(basename "$skill_path")"
  echo "Packaging $skill ..."
  # Zip from inside SKILLS_DIR so archive paths are <skill>/... (no leading dirs).
  ( cd "$SKILLS_DIR" && zip -r -q "$OUT_ABS/$skill.zip" "$skill" -x "${EXCLUDES[@]}" )
  count=$((count + 1))
done

if [[ "$count" -eq 0 ]]; then
  echo "error: no skills found under $SKILLS_DIR" >&2
  exit 1
fi

# Integrity manifest (paths relative to dist/).
( cd "$OUT_DIR" && sha256sum ./*.zip > SHA256SUMS.txt )

echo
echo "Packaged $count skill(s) into $OUT_DIR/:"
ls -1 "$OUT_DIR"
