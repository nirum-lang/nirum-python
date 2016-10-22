#!/usr/bin/env bash
set -e

flake8 .

if [[ "$(python -c "import sys;print(sys.version[0])")" != "2" ]]; then
  import-order nirum ./nirum
fi
