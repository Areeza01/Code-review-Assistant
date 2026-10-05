import os

from dotenv import load_dotenv
from azure.ai.projects import AIProjectClient
from azure.identity import DefaultAzureCredential

load_dotenv()

project_client = AIProjectClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

client = project_client.get_openai_client()


def generate_review(code, findings):

    prompt = f"""
Static Analysis Findings:
{findings}

Source Code:
{code}

Review the code and provide:
- Summary
- Bugs Found
- Security Risks
- Performance Issues
- Code Quality Observations
- Best Practices Recommendations
- Refactoring Suggestions
- Positive Aspects
- Overall Score
- Final Verdict
"""

    response = client.responses.create(
        model="gpt-4.1",
        input=prompt
    )

    return response.output_text