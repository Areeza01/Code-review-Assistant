import ast


def analyze_python(code):

    issues = []

    try:

        tree = ast.parse(code)

        for node in ast.walk(tree):

            if isinstance(node, ast.FunctionDef):

                if len(node.body) > 20:

                    issues.append(
                        f"Large function detected: {node.name}"
                    )

    except Exception as e:

        issues.append(str(e))

    return issues


def analyze_javascript(code):

    issues = []

    if "eval(" in code:
        issues.append("Use of eval() detected")

    if "var " in code:
        issues.append(
            "Use let or const instead of var"
        )

    return issues
