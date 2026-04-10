#!/usr/bin/env bash
# ContractLens — first-time setup
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== ContractLens Setup ==="

# ── Backend ────────────────────────────────────────────────────────────────────
echo ""
echo "[1/3] Setting up Python virtual environment..."
cd "$SCRIPT_DIR/backend"

python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt
echo "      ✓ Python deps installed"

deactivate

# ── Frontend ───────────────────────────────────────────────────────────────────
echo ""
echo "[2/3] Installing frontend dependencies..."
cd "$SCRIPT_DIR/frontend"
npm install
echo "      ✓ npm deps installed"

# ── Done ───────────────────────────────────────────────────────────────────────
echo ""
echo "[3/3] Setup complete!"
echo ""
echo "  Start backend : cd backend && source venv/bin/activate && uvicorn main:app --reload"
echo "  Start frontend: cd frontend && npm run dev"
echo ""
echo "  Or just run:    ./start.sh"
