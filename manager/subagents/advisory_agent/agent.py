from google.adk.agents import Agent

from . import calculator
from .tools.rag_query import rag_query
from .tools.google_search import google_search_agent
from google.adk.tools.agent_tool import AgentTool
from dotenv import load_dotenv
load_dotenv()

def calculate_solar_details(monthly_bill: int) -> dict:
    """
    Calculate solar panel installation details based on user inputs.
    Returns details for both with and without subsidy options.
    """
    # Calculate for both subsidy options
    results = {}
    # Hardcode pincode for hackathon purpose.
    pincode = 515002
    #total_units_used = calculator.calculate_unit_used(monthly_bill, pincode) 
    total_units_used = calculator.calculate_unit_used(monthly_bill, pincode)
    
    if total_units_used is None:
        return {"error": "Invalid pincode or location not supported"}
    
    # Create results for both subsidy options
    for subsidy_option in ["with_subsidy", "without_subsidy"]:
        has_subsidy = subsidy_option == "with_subsidy"
        
        results[subsidy_option] = {
            "num_panels": calculator.number_of_solar_panels(subsidy_option, pincode, total_units_used),
            "area_needed_sqft": calculator.area_needed_in_sqft(subsidy_option, pincode, total_units_used),
            "yearly_savings": calculator.savings_on_electricity_per_year(monthly_bill),
            "yearly_power_generation": calculator.generate_power_kwh_per_year(subsidy_option, pincode, total_units_used),
            "recovery_years": calculator.total_overall_cost(subsidy_option, pincode, total_units_used) / calculator.savings_on_electricity_per_year(monthly_bill),
            "daily_energy_production": calculator.total_energy_produced_daily(subsidy_option, pincode, total_units_used),
            "system_size_kw": calculator.total_kwh_setup(subsidy_option, pincode, total_units_used) / 1000,
            "co2_reduction_tons": calculator.co2_cut_in_tons(subsidy_option, total_units_used),
            "costs": {
                "panels": calculator.cost_of_panels(subsidy_option, pincode, total_units_used),
                "inverter": calculator.setup_cost(subsidy_option, pincode, total_units_used, "inverter"),
                "mounting": calculator.setup_cost(subsidy_option, pincode, total_units_used, "mounting"),
                "distribution_boxes": calculator.setup_cost(subsidy_option, pincode, total_units_used, "dc_db") + calculator.setup_cost(subsidy_option, pincode, total_units_used, "ac_db"),
                "cables": calculator.setup_cost(subsidy_option, pincode, total_units_used, "dc_cable") + calculator.setup_cost(subsidy_option, pincode, total_units_used, "ac_cable"),
                "earthing_kit": calculator.setup_cost(subsidy_option, pincode, total_units_used, "earthing_kit"),
                "lightning_arrestor": calculator.setup_cost(subsidy_option, pincode, total_units_used, "lightning_arrester"),
                "net_meter": calculator.setup_cost_constants["net_meter"],
                "accessories": calculator.setup_cost(subsidy_option, pincode, total_units_used, "connectors") + 
                              calculator.setup_cost(subsidy_option, pincode, total_units_used, "cable_ties") + 
                              calculator.setup_cost(subsidy_option, pincode, total_units_used, "installation_accessories"),
                "labor": calculator.setup_cost(subsidy_option, pincode, total_units_used, "labour_and_installation"),
                "gst": calculator.gst(subsidy_option, pincode, total_units_used),
                "subsidy": calculator.government_subsidy(subsidy_option, pincode, total_units_used),
                "total": calculator.total_overall_cost(subsidy_option, pincode, total_units_used)
            }
        }
    
    return results

advisory_agent = Agent(
    name="advisory_agent",
    model="gemini-2.0-flash",
    description="Advisory agent",
    instruction="""
        You are a helpful solar advisor agent that provides information to the user and can calculate solar panel requirements, costs, and potential savings based on user inputs.
        The context for rag query on solar panel data will be provided by the following tool:
        - rag_query: This tool allows you to query a RAG corpus and retrieve relevant information.

        Tools:
        - google_search_agent: This tool allows you to search the web for information.
        - rag_query: This tool allows you to query a RAG corpus and retrieve relevant information.
        - calculate_solar_details: This tool allows you to calculate solar panel requirements, costs, and potential savings based on user inputs.

        You can use the calculate_solar_details tool to calculate solar panel requirements, costs, and potential savings based on user inputs.
        You can use the google_search_agent to search for information if the context is not sufficient.

        You can use the rag_query tool to query a RAG corpus and retrieve relevant information. In that case, you will be provided with a context and a question. Your task is to answer the question based on the context.
        If you are unable to answer the question based on the context, just say "I am unable to answer the question based on the context. Please try again later.".
    """,
    tools=[AgentTool(google_search_agent), rag_query, calculate_solar_details]
)