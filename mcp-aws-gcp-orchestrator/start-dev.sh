#!/bin/bash

# Start development servers

echo "🚀 Starting MCP Orchestrator Development Environment"

# Start backend in background
echo "📡 Starting FastAPI backend..."
cd backend
python3 -m uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 3

# Start React frontend
echo "⚛️ Starting React frontend..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Development servers started!"
echo "📡 Backend: http://localhost:8000"
echo "⚛️ Frontend: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop all servers"

# Wait for user interrupt
trap "echo '🛑 Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
