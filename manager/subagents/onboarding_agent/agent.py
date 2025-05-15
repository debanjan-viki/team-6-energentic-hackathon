from google.adk.agents import Agent
from dotenv import load_dotenv

from enrollment import Enrollment
load_dotenv()

def handle_enrollment(energy_resource_id: str) -> dict:
    """
    Handles the enrollment process by creating and toggling DER.

    Args:
        energy_resource_id (str): The ID of the energy resource.

    Returns:
        dict: The response from the DER creation and toggling process.
    """
    enrollment = Enrollment()
    return enrollment.create_and_toggle_der(energy_resource_id)

onboarding_agent = Agent(
    name="onboarding_agent",
    model="gemini-2.0-flash",
    description="Onboarding agent",
    instruction="""
        You are an enrollment agent that is responsible for overseeing the work of the other agents.

        Always delegate the task to the appropriate agent. Use your best judgement 
        to determine which agent to delegate to.

        You are responsible for delegating tasks to the following agents:
        - enrollment: Provides information about enrollment and DER switching.

        If the task is related to enrollment, delegate it to the enrollment agent.
        After delegating the task, wait for the response from the agent and return it to the user and always come back to the manager agent after the task is done.
        If you are unable to delegate the task to any agent, and say "I am unable to delegate the task to any agent. Please try again later.".
    """,
    sub_agents=[handle_enrollment],
)