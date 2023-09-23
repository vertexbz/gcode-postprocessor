#!/bin/sh
_DIR=$(cd "$(dirname "$0")"; pwd)
VENV="${_DIR}/.venv"
PYTHON="${VENV}/bin/python3"

if [ ! -x "${PYTHON}" ]; then
  python3 -m venv "${VENV}"
  "${VENV}/bin/pip" install -r "${_DIR}/requirements.txt"
fi

exec "${PYTHON}" "${_DIR}/main.py" "$@"
