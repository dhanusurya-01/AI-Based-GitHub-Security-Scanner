import requests

OLLAMA_URL = "http://localhost:11434/api/generate"


def local_explainer(vuln_type):
    data = {
        "HARDCODED_PASSWORD": """
🔴 WHAT IS:
Password stored directly in code.

⚠️ WHY:
Anyone can read and use it.

🧑‍💻 HACKER STEPS:
1. Read source code
2. Find password
3. Login

💥 IMPACT:
Unauthorized access.

🛠️ FIX:
Use environment variables.

✅ CODE:
import os
password = os.getenv("PASSWORD")
""",

        "HARDCODED_SECRET": """
🔴 WHAT IS:
API keys or tokens stored in code.

⚠️ WHY:
Anyone can steal and misuse them.

🧑‍💻 HACKER STEPS:
1. Read code
2. Copy key
3. Use API


💥 IMPACT:
Account/API misuse.

🛠️ FIX:
Store secrets securely.

✅ CODE:
import os
api_key = os.getenv("API_KEY")
""",

        "DANGEROUS_EVAL": """
🔴 WHAT IS:
eval() executes user input as code.

⚠️ WHY:
Attacker can run malicious commands.

🧑‍💻 HACKER STEPS:
1. Input malicious code
2. eval executes it
3. System compromised

💥 IMPACT:
Full system control.

🛠️ FIX:
Avoid eval(), validate input.

✅ CODE:
# safer alternative
""",

        "DANGEROUS_EXEC": """
🔴 WHAT IS:
exec() runs dynamic code.

⚠️ WHY:
Attacker can execute any command.

🧑‍💻 HACKER STEPS:
1. Inject code
2. exec runs it
3. System compromised

💥 IMPACT:
Full system control.

🛠️ FIX:
Avoid exec().

✅ CODE:
# avoid exec
""",

        "COMMAND_INJECTION": """
🔴 WHAT IS:
User input passed to system command.

⚠️ WHY:
Attacker can run OS commands.

🧑‍💻 HACKER STEPS:
1. Input malicious command
2. system executes
3. Gain access

💥 IMPACT:
System takeover.

🛠️ FIX:
Use safe methods.

✅ CODE:
subprocess.run(["echo", user_input])
""",

        "UNSAFE_DESERIALIZATION": """
🔴 WHAT IS:
pickle.load() loads unsafe data.

⚠️ WHY:
Malicious code can execute.

🧑‍💻 HACKER STEPS:
1. Send malicious file
2. Load with pickle
3. Code executes

💥 IMPACT:
Remote code execution.

🛠️ FIX:
Use safe formats like JSON.

✅ CODE:
import json
data = json.load(f)
""",

        "WEAK_RANDOM_USAGE": """
🔴 WHAT IS:
Using random() for security.

⚠️ WHY:
Predictable values.

🧑‍💻 HACKER STEPS:
1. Predict output
2. Break security

💥 IMPACT:
Security failure.

🛠️ FIX:
Use secure random.

✅ CODE:
import secrets
secrets.token_hex(16)
""",

        "INSECURE_HTTP": """
🔴 WHAT IS:
Using HTTP instead of HTTPS.

⚠️ WHY:
Data is not encrypted.

🧑‍💻 HACKER STEPS:
1. Intercept traffic
2. Read data

💥 IMPACT:
Data leak.

🛠️ FIX:
Use HTTPS.

✅ CODE:
https://example.com
"""
    }

    return data.get(vuln_type, "⚠ Unknown vulnerability")


def explain_vulnerability(vuln_type, code_snippet, file_path):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": "mistral",
                "prompt": f"Explain {vuln_type} simply",
                "stream": False
            },
            timeout=5
        )

        return response.json().get("response", local_explainer(vuln_type))

    except Exception:
        # 🔥 NO ERROR MESSAGE — clean fallback
        return local_explainer(vuln_type)