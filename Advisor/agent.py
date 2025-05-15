from google.adk.agents import Agent
from dotenv import load_dotenv
load_dotenv()

root_agent = Agent(
    name="Advisor_agent",
    model="gemini-2.0-flash",
    description="Advisor agent",
    instruction="""
        You are a helpful Advisor agent that provides Solar advice and information.
    """)