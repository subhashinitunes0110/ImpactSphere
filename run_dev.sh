trap "kill 0" EXIT
echo"======================================="
echo "Starting Backend (FastAPI on http://127.0.0.1:8000)"
echo "========================================"
cd backend
puthon -m uvicorn app.main:app --reload --port 8000 &
echo "==========================================="
echo "Starting Frontend (Next.js on http://localhost:3000)"
echo "========================================"
cd ../frontend
npm run dev &
wait
