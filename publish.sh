#!/usr/bin/env bash
#
# Build and publish novant to PyPI.
#
# Reads PyPI token from secret/api.key (gitignored).
# Version is read from pyproject.toml (the single source of truth).
#

set -euo pipefail

cd "$(dirname "$0")"

token_file="secret/api.key"
if [[ ! -f "$token_file" ]]; then
  echo "error: PyPI token not found at $token_file" >&2
  exit 1
fi

version=$(grep -E '^version = ' pyproject.toml | sed -E 's/version = "(.+)"/\1/')

# Use the project's venv if present, otherwise the active python.
if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
else
  PY=python
fi

if ! "$PY" -c "import build, twine" 2>/dev/null; then
  echo "error: 'build' and/or 'twine' not available on $PY" >&2
  echo "  set up the venv with:" >&2
  echo "    python3 -m venv .venv" >&2
  echo "    source .venv/bin/activate" >&2
  echo "    pip install -e \".[dev]\"" >&2
  exit 1
fi

echo "Publishing novant $version to PyPI"
read -r -p "Continue? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "aborted"
  exit 1
fi

rm -rf dist/ build/ novant.egg-info/
"$PY" -m build

TWINE_USERNAME=__token__ \
TWINE_PASSWORD="$(cat "$token_file")" \
  "$PY" -m twine upload dist/*

git tag "v$version"
git push --tags

echo "published novant $version"
