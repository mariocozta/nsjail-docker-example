import sys
import json
import io
import contextlib

if len(sys.argv) != 2:
    print(json.dumps({"error": "Missing script path"}))
    sys.exit(1)

script_path = sys.argv[1]

try:
    with open(script_path, "r") as f:
        code = compile(f.read(), script_path, 'exec')
        scope = {}

        stdout_capture = io.StringIO()

        with contextlib.redirect_stdout(stdout_capture):
            exec(code, scope)
            if "main" not in scope or not callable(scope["main"]):
                print(json.dumps({"error": "No valid main() found"}))
                sys.exit(1)
            result = scope["main"]()

        output = {
            "result": result,
            "stdout": stdout_capture.getvalue()
        }
        print(json.dumps(output))

except Exception as e:
    print(json.dumps({"error": str(e)}))
    sys.exit(1)
