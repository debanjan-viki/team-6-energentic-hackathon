from google.adk.agents import Agent
from google.adk.tools import google_search

google_search_agent = Agent(
    name="google_search_agent",
    model="gemini-2.0-flash",
    description="Google search agent",
    instruction="""
    You are a helpful assistant that can analyze news articles and information on solar and renewables and provide a summary of the news.

    When asked about news, you should use the google_search tool to search for the news.
    """,
    tools=[google_search],
)