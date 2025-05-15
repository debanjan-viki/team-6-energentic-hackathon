from google.adk.agents import Agent
from dotenv import load_dotenv

from .subagents.financial_agent.agent import financial_agent
from .subagents.advisory_agent.agent import advisory_agent
from .subagents.onboarding_agent.agent import onboarding_agent
load_dotenv()

root_agent = Agent(
    name="manager",
    model="gemini-2.0-flash",
    description="Manager agent",
    instruction="""
        You are a manager agent that is responsible for overseeing the work of the other agents.

        Always delegate the task to the appropriate agent. Use your best judgement 
        to determine which agent to delegate to.

        You are responsible for delegating tasks to the following agents:
        - onboarding_agent: Provides information and help users about DER enrollment and DER switching.
        - advisory_agent: Provides information from the RAG corpus in google cloud (about solar and renewables) or search google in real time.

        If the task is related to solar and renewables, delegate it to the rag agent.
        After delegating the task, wait for the response from the agent and return it to the user and always come back to the manager agent after the task is done.
        If you are unable to delegate the task to any agent, and say "I am unable to delegate the task to any agent. Please try again later.".
    """,
    sub_agents=[onboarding_agent, advisory_agent],
)