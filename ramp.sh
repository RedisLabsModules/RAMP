#!/bin/bash

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
PYTHONPATH="$HERE" python "$HERE/RAMP/ramp.py" "$@"
