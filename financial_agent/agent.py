from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

root_agent = Agent(
    name="financial_agent",
    model="gemini-2.0-flash",
    description="Financial agent",
    instruction="""
        You are a helpful financial agent that provides financial advice and information.
    """)