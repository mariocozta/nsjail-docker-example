import os
import tempfile
import subprocess
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

NSJAIL_PATH = "/usr/local/bin/nsjail"
NSJAIL_CFG = "/config/nsjail.cfg"
PYTHON_RUNNER = "/sandbox/runner.py"
USE_NSJAIL = os.getenv("USE_NSJAIL", "true").lower() == "true"

@app.route("/execute", methods=["POST"])
def execute():
    data = request.get_json()
    if not data or "script" not in data:
        return jsonify({"error": "Missing 'script' field"}), 400

    script_code = data["script"]

    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".py", dir="/sandbox") as f:
        script_path = f.name
        f.write(script_code)

    try:
        if USE_NSJAIL:
            cmd = [
                NSJAIL_PATH,
                "--config", NSJAIL_CFG,
                "--",
                "/usr/bin/python3",
                PYTHON_RUNNER,
                script_path
            ]
        else:
            cmd = ["/usr/bin/python3", PYTHON_RUNNER, script_path]

        proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)

        try:
            parsed = json.loads(proc.stdout.decode())
        except Exception:
            return jsonify({
                "error": "Invalid script output",
                "raw_stdout": proc.stdout.decode(),
                "stderr": proc.stderr.decode()
            }), 400

        return jsonify(parsed)

    except subprocess.TimeoutExpired:
        return jsonify({"error": "Execution timed out"}), 408
    finally:
        os.remove(script_path)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
