import subprocess
import time

# Start backend using Python module execution
backend = subprocess.Popen([
    "python", "-m", "uvicorn", "backend.app:app", "--port", "8000"
])
time.sleep(2)

# Start frontend (Streamlit)
frontend = subprocess.Popen(["streamlit", "run", "ui.py"])

try:
    backend.wait()
    frontend.wait()
except KeyboardInterrupt:
    print("Shutting down both servers...")
    backend.terminate()
    frontend.terminate()
