#!/usr/bin/env bash

# === Setup Script cho tất cả MCP Servers ===
# Lệnh này sẽ tự động tìm tất cả các thư mục có Makefile và chạy lệnh "make setup"

set -e

# Lấy thư mục gốc chứa file script này
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "[INFO] Đang cài đặt tất cả MCP Servers trong $ROOT_DIR..."

cd "$ROOT_DIR"

# Tìm các thư mục con có chứa Makefile
for D in */; do
    if [ -f "${D}Makefile" ]; then
        echo "============================================"
        echo "[INFO] Đang thiết lập MCP Server: ${D%/}"
        cd "${D}"
        make setup
        echo "[SUCCESS] Thiết lập xong: ${D%/}"
        cd "$ROOT_DIR"
        echo "============================================"
    fi
done

echo "[MAINTENANCE] Tất cả các MCP Servers đã được cài đặt môi trường ảo (.venv) thành công!"
echo "[MAINTENANCE] Bạn có thể cung cấp file mcp-config.json cho IDE / Agent (Antigravity/Cursor/Claude) để chúng tự động spawn tất cả server này."
