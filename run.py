import subprocess
import sys
import os
import signal
import threading

ROOT = os.path.dirname(os.path.abspath(__file__))
BACKEND_DIR = os.path.join(ROOT, "backend")
FRONTEND_DIR = os.path.join(ROOT, "frontend")

processes = []
BACKEND_PORT = 8003


def free_port(port: int):
    if sys.platform != "win32":
        return
    try:
        result = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True, text=True
        )
        pids = set()
        for line in result.stdout.splitlines():
            if f":{port}" in line and "LISTENING" in line:
                parts = line.strip().split()
                if parts:
                    pids.add(parts[-1])
        for pid in pids:
            try:
                subprocess.run(["taskkill", "/F", "/PID", pid],
                               capture_output=True)
                print(f"[run.py] Killed PID {pid} holding port {port}")
            except Exception:
                pass
        if pids:
            import time
            time.sleep(1)
    except Exception as e:
        print(f"[run.py] Could not free port {port}: {e}")


def stream_output(proc, prefix):
    for line in iter(proc.stdout.readline, b""):
        print(f"[{prefix}] {line.decode(errors='replace').rstrip()}", flush=True)


def shutdown(signum, frame):
    print("\n[run.py] Shutting down all processes...")
    for p in processes:
        p.terminate()
    sys.exit(0)


signal.signal(signal.SIGINT, shutdown)
signal.signal(signal.SIGTERM, shutdown)


def start_backend():
    free_port(BACKEND_PORT)
    print(f"[run.py] Starting backend on http://localhost:{BACKEND_PORT} ...")
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.Popen(
        [sys.executable, "-m", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", str(BACKEND_PORT)],
        cwd=BACKEND_DIR,
        env=env,
    )
    processes.append(proc)
    return proc


def start_frontend():
    print("[run.py] Starting frontend on http://localhost:8080 ...")
    npm_cmd = "npm.cmd" if sys.platform == "win32" else "npm"
    proc = subprocess.Popen(
        [npm_cmd, "run", "dev"],
        cwd=FRONTEND_DIR,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    processes.append(proc)
    threading.Thread(target=stream_output, args=(proc, "FRONTEND"), daemon=True).start()
    return proc


if __name__ == "__main__":
    backend = start_backend()
    frontend = start_frontend()

    print("[run.py] Both services started. Press Ctrl+C to stop.")
    print("[run.py] Backend logs print directly. Frontend logs prefixed [FRONTEND].\n")

    try:
        while backend.poll() is None:
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        shutdown(None, None)
