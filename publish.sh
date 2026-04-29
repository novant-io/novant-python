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

echo "Publishing novant $version to PyPI"
read -r -p "Continue? [y/N] " confirm
if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
  echo "aborted"
  exit 1
fi

rm -rf dist/ build/ novant.egg-info/
python -m build

TWINE_USERNAME=__token__ \
TWINE_PASSWORD="$(cat "$token_file")" \
  python -m twine upload dist/*

git tag "v$version"
git push --tags

echo "published novant $version"
