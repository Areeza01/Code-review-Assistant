from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential
import os

client = AgentsClient(
    endpoint=os.getenv("PROJECT_ENDPOINT"),
    credential=DefaultAzureCredential()
)

agent = client.create_agent(
    model="gpt-4o",
    name="Recruitment-Resume-Analyzer",
    instructions="""
You are an HR Resume Screening Assistant.

Return ONLY JSON:

{
    "score": 0,
    "recommendation": "",
    "strengths": [],
    "weaknesses": [],
    "matched_skills": [],
    "missing_skills": []
}
"""
)

print("Agent Created")
print("ID:", agent.id)