#!/usr/bin/env bash
# Start both backend and frontend in separate terminals (requires gnome-terminal / bash)
set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# ── Backend ────────────────────────────────────────────────────────────────────
echo "Starting backend on http://localhost:8000 ..."
gnome-terminal --title="ContractLens Backend" -- bash -c "
  cd '$SCRIPT_DIR/backend'
  source venv/bin/activate
  uvicorn main:app --reload --port 8000
  exec bash
" 2>/dev/null || (
  # Fallback: start in background if gnome-terminal is unavailable
  cd "$SCRIPT_DIR/backend"
  source venv/bin/activate
  uvicorn main:app --reload --port 8000 &
  BACKEND_PID=$!
  echo "  Backend PID: $BACKEND_PID"
  deactivate
  cd "$SCRIPT_DIR"
)

# ── Frontend ───────────────────────────────────────────────────────────────────
echo "Starting frontend on http://localhost:5173 ..."
gnome-terminal --title="ContractLens Frontend" -- bash -c "
  cd '$SCRIPT_DIR/frontend'
  npm run dev
  exec bash
" 2>/dev/null || (
  cd "$SCRIPT_DIR/frontend"
  npm run dev
)

echo ""
echo "ContractLens is running:"
echo "  Frontend → http://localhost:5173"
echo "  Backend  → http://localhost:8000"
echo "  API docs → http://localhost:8000/docs"
