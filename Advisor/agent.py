# from google.adk.agents import Agent
# from dotenv import load_dotenv
# import os
# from . import calculator

# load_dotenv()

# def calculate_solar_details(monthly_bill: int, pincode: int, want_subsidy: bool = True) -> dict:
#     """
#     Calculate solar panel installation details based on user inputs.
#     """
#     subsidy_type = "with_subsidy" if want_subsidy else "without_subsidy"
#     total_units_used = calculator.calculate_unit_used(monthly_bill, pincode)
    
#     if total_units_used is None:
#         return {"error": "Invalid pincode or location not supported"}
    
#     results = {
#         "num_panels": calculator.number_of_solar_panels(subsidy_type, pincode, total_units_used),
#         "area_needed_sqft": calculator.area_needed_in_sqft(subsidy_type, pincode, total_units_used),
#         "yearly_savings": calculator.savings_on_electricity_per_year(monthly_bill),
#         "yearly_power_generation": calculator.generate_power_kwh_per_year(subsidy_type, pincode, total_units_used),
#         "recovery_years": calculator.total_overall_cost(subsidy_type, pincode, total_units_used) / calculator.savings_on_electricity_per_year(monthly_bill),
#         "daily_energy_production": calculator.total_energy_produced_daily(subsidy_type, pincode, total_units_used),
#         "system_size_kw": calculator.total_kwh_setup(subsidy_type, pincode, total_units_used) / 1000,
#         "co2_reduction_tons": calculator.co2_cut_in_tons(subsidy_type, total_units_used),
#         "costs": {
#             "panels": calculator.cost_of_panels(subsidy_type, pincode, total_units_used),
#             "inverter": calculator.setup_cost(subsidy_type, pincode, total_units_used, "inverter"),
#             "mounting": calculator.setup_cost(subsidy_type, pincode, total_units_used, "mounting"),
#             "distribution_boxes": calculator.setup_cost(subsidy_type, pincode, total_units_used, "dc_db") + calculator.setup_cost(subsidy_type, pincode, total_units_used, "ac_db"),
#             "cables": calculator.setup_cost(subsidy_type, pincode, total_units_used, "dc_cable") + calculator.setup_cost(subsidy_type, pincode, total_units_used, "ac_cable"),
#             "earthing_kit": calculator.setup_cost(subsidy_type, pincode, total_units_used, "earthing_kit"),
#             "lightning_arrestor": calculator.setup_cost(subsidy_type, pincode, total_units_used, "lightning_arrester"),
#             "net_meter": calculator.setup_cost_constants["net_meter"],
#             "accessories": calculator.setup_cost(subsidy_type, pincode, total_units_used, "connectors") + 
#                           calculator.setup_cost(subsidy_type, pincode, total_units_used, "cable_ties") + 
#                           calculator.setup_cost(subsidy_type, pincode, total_units_used, "installation_accessories"),
#             "labor": calculator.setup_cost(subsidy_type, pincode, total_units_used, "labour_and_installation"),
#             "gst": calculator.gst(subsidy_type, pincode, total_units_used),
#             "subsidy": calculator.government_subsidy(subsidy_type, pincode, total_units_used),
#             "total": calculator.total_overall_cost(subsidy_type, pincode, total_units_used)
#         }
#     }
    
#     return results

# root_agent = Agent(
#     name="Advisor_Agent",
#     model="gemini-2.0-flash",
#     description="Advisor agent",
#     instruction="""
#         You are a helpful Solar Advisor agent that provides solar advice and information.
#         You can calculate solar panel requirements, costs, and potential savings based on user inputs.
        
#         Always be polite and professional. If you don't know something, say so.
#         Focus on helping users understand if solar panels are a good investment for them.
#         You also have access to a solar calculator that can provide detailed information about solar panel installation.
#     """,
#     tools=[calculate_solar_details],
# )




from google.adk.agents import Agent
from dotenv import load_dotenv
import os
from . import calculator

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

root_agent = Agent(
    name="Solar_Advisor_Agent",
    model="gemini-2.0-flash",
    description="Solar advisor agent",
    instruction="""
        You are a helpful Solar Advisor agent that provides solar panel installation advice and information.
        You can calculate solar panel requirements, costs, and potential savings based on user inputs.
        
        Always be polite and professional. If you don't know something, say so.
        Focus on helping users understand if solar panels are a good investment for them.
        
        IMPORTANT: When a user provides their electricity bill, ALWAYS provide analysis for 
        BOTH subsidy and non-subsidy options without asking the user to choose. Present a comparison 
        showing the benefits of each option.
        
        Include the following key metrics in your response:
        1. Number of panels required
        2. Area needed (in sq ft)
        3. System size (in kW)
        4. Yearly power generation
        5. Yearly savings on electricity bills
        6. CO2 emission reduction per year
        7. Total costs (with breakdown)
        8. Payback period (recovery years)
        
        Format the comparison in a clear, easy-to-understand way, highlighting the differences between 
        subsidy and non-subsidy options.
    """,
    tools=[calculate_solar_details],
)