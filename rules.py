import re


def check_file(file_path):
    """
    Read file and send each line for analysis
    """
    issues = []

    try:
        with open(file_path, "r", errors="ignore") as f:
            lines = f.readlines()
    except Exception:
        return issues

    for line_no, line in enumerate(lines, start=1):

        # 1. Hardcoded password
        if re.search(r'password\s*=\s*["\'].*["\']', line, re.IGNORECASE):
            issues.append(("HARDCODED_PASSWORD", line_no, line.strip()))

        # 2. Hardcoded secrets
        if re.search(r'(api_key|secret|token)\s*=\s*["\'].*["\']', line, re.IGNORECASE):
            issues.append(("HARDCODED_SECRET", line_no, line.strip()))

        # 3. eval usage
        if re.search(r'\beval\s*\(', line):
            issues.append(("DANGEROUS_EVAL", line_no, line.strip()))

        # 4. exec usage
        if re.search(r'\bexec\s*\(', line):
            issues.append(("DANGEROUS_EXEC", line_no, line.strip()))

        # 5. SQL Injection risk
        if re.search(r'execute\s*\(.*\+.*\)', line):
            issues.append(("SQL_INJECTION_RISK", line_no, line.strip()))

        # 6. Command Injection
        if re.search(r'os\.system\s*\(', line):
            issues.append(("COMMAND_INJECTION", line_no, line.strip()))

        # 7. Unsafe subprocess
        if re.search(r'subprocess\.Popen\s*\(', line):
            issues.append(("UNSAFE_SUBPROCESS", line_no, line.strip()))

        # 8. Unsafe deserialization
        if re.search(r'pickle\.load\s*\(', line):
            issues.append(("UNSAFE_DESERIALIZATION", line_no, line.strip()))

        # 9. Debug mode
        if re.search(r'debug\s*=\s*True', line):
            issues.append(("DEBUG_MODE_ON", line_no, line.strip()))

        # 10. Insecure HTTP
        if re.search(r'http://', line):
            issues.append(("INSECURE_HTTP", line_no, line.strip()))

        # 11. Hidden exception
        if re.search(r'except\s*:\s*pass', line):
            issues.append(("HIDDEN_EXCEPTION", line_no, line.strip()))

        # 12. Weak random
        if re.search(r'random\.random\s*\(', line):
            issues.append(("WEAK_RANDOM_USAGE", line_no, line.strip()))

    return issues