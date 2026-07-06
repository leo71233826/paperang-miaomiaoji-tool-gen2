#!/usr/bin/env bash
# Paperang 喵喵机 - 快速启动脚本
# 由 setup_env.py 自动生成

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_PYTHON="/workspace/.venv/bin/python"

echo "🖨️  启动 Paperang 喵喵机..."
"$VENV_PYTHON" "$SCRIPT_DIR/run_paperang.py" "$@"
