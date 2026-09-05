#!/bin/bash
set -euo pipefail

export PYTHONWARNINGS="ignore"

# Prevent a real browser from being discovered for Apps that request `open=True`.
# We never want it during the docs build
# we use `true`, as it should always be available, and always give a '0' exit code
export BROWSER='true'

cd "$(dirname "$0")"

# Each notebook gets its own kernel, and the build is dominated by kernel start-up
# plus imports rather than by the cells themselves, so this scales close to linearly.
JOBS="${JOBS:-$( { command -v nproc >/dev/null && nproc; } || sysctl -n hw.logicalcpu 2>/dev/null || echo 4 )}"

# Resolve the interpreter once, rather than paying `uv run`'s lockfile check per notebook.
PY="$(uv run python -c 'import sys; print(sys.executable)')"

# remove artifacts before building
find docs -type f \( -name '*.html' -o -name '*-preview.png' \) -delete

find docs -type f -name '*.ipynb' -not -path '*.ipynb_checkpoints*' -print0 \
  | xargs -0 -n1 -P"$JOBS" "$PY" -m nbconvert --to notebook --inplace \
      --ExecutePreprocessor.timeout=-1 \
      --ClearMetadataPreprocessor.enabled=True \
      --ClearMetadataPreprocessor.preserve_cell_metadata_mask tags \
      --execute
