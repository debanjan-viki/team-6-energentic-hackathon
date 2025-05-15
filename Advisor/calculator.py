import json
import math
import os

# Load data files from the same directory as this script
def load_json_data(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'data', filename)
    with open(file_path, 'r') as file:
        return json.load(file)

# Load data
state_wise_data = load_json_data('dataset_solar_calculator.json')
price_chart = load_json_data('price_chart.json')
panel_constants = load_json_data('panel_constants.json')
setup_cost_constants = load_json_data('setup_cost_constants.json')

def get_field_from_json(field_to_match, value_to_match, return_field):
    for entry in state_wise_data:
        if entry[field_to_match] == value_to_match:
            return entry[return_field]
    return None

def calculate_unit_used(total_bill, pincode):
    state = get_field_from_json("Pincode", pincode, "StateoRuT")
   
    if state is None:
        return None
    
    total_bill = total_bill * 0.97
    prices = price_chart[state]
    i = 0
    total_units = 0

    while (total_bill > 0): 
        remaining = total_bill - (prices[i] * 50)
        if (remaining < 0):
            total_units += (total_bill / prices[i])
            break
        else:
            total_bill -= (prices[i] * 50)
            total_units += 50
            if (i != len(prices) - 1):
                i += 1

    return total_units

def daily_consumption(total_units_consumed):
    return total_units_consumed / 30

def temperature_factor(type, pincode):
    temp = get_field_from_json("Pincode", pincode, "Avg Tmp")
    temp_coeff = panel_constants["temperature_coefficient"][type]
    return 1 + (temp_coeff * (temp - 25))

def shading_factor(pincode):
    return get_field_from_json("Pincode", pincode, "Shading Factor")

def soiling_factor(pincode):
    return get_field_from_json("Pincode", pincode, "Soiling Factor")

def average_irradiance(pincode):
    return get_field_from_json("Pincode", pincode, "Average Irradiance")

def derating_factor(type, pincode):
    return temperature_factor(type, pincode) * shading_factor(pincode) * soiling_factor(pincode) * panel_constants["inverter_efficiency"][type] * panel_constants["installation_quality_factor"][type]

def theoretical_daily_energy(type, pincode):
    return panel_constants["panel_efficiency"][type] * panel_constants["panel_area_m2"][type] * average_irradiance(pincode)

def adjusted_daily_energy(type, pincode):
    return theoretical_daily_energy(type, pincode) * derating_factor(type, pincode)

def number_of_solar_panels(type, pincode, total_units_consumed):
    res = daily_consumption(total_units_consumed) / adjusted_daily_energy(type, pincode)
    return math.ceil(res)

def total_energy_produced_daily(type, pincode, total_units_consumed):
    return number_of_solar_panels(type, pincode, total_units_consumed) * adjusted_daily_energy(type, pincode)

def total_kwh_setup(type, pincode, total_units_consumed):
    return number_of_solar_panels(type, pincode, total_units_consumed) * panel_constants["panel_wp"][type]

def co2_cut_in_tons(type, total_units_consumed):
    return (panel_constants["co2_emission_factor"][type] * daily_consumption(total_units_consumed) * 365) / 1000

def area_needed_in_sqft(type, pincode, total_units_consumed):
    return number_of_solar_panels(type, pincode, total_units_consumed) * panel_constants["panel_area"][type]

def savings_on_electricity_per_year(total_bill):
    return 12 * total_bill

def generate_power_kwh_per_year(type, pincode, total_units_consumed):
    return number_of_solar_panels(type, pincode, total_units_consumed) * adjusted_daily_energy(type, pincode) * 365

def cost_of_panels(type, pincode, total_units_consumed):
    return number_of_solar_panels(type, pincode, total_units_consumed) * panel_constants["single_panel_costs"][type]

def setup_cost(type, pincode, total_units_consumed, field):
    return total_kwh_setup(type, pincode, total_units_consumed) * setup_cost_constants[field]

def total_setup_cost(type, pincode, total_units_consumed):
    total = 0

    total += cost_of_panels(type, pincode, total_units_consumed)

    total += setup_cost_constants["net_meter"]

    fields = ["inverter", 
        "mounting",
        "dc_db",
        "ac_db",
        "dc_cable",
        "ac_cable",
        "earthing_kit",
        "lightning_arrester",
        "connectors",
        "cable_ties",
        "installation_accessories",
        "labour_and_installation"
    ]

    for field in fields:
        total += setup_cost(type, pincode, total_units_consumed, field)
    
    return total

def gst(type, pincode, total_units_consumed):
    total = total_setup_cost(type, pincode, total_units_consumed)
    return (0.7 * total * 0.12) + (0.3 * total * 0.18)
    
def government_subsidy(type, pincode, total_units_consumed):
    if (type == "without_subsidy"):
        return 0
    
    total_kwh_setup_amount = total_kwh_setup(type, pincode, total_units_consumed)

    if ((total_kwh_setup_amount / 1000) >= 3):
        return 78000
    
    if ((total_kwh_setup_amount / 1000) > 2):
        return 60000 + (((total_kwh_setup_amount / 1000) - 2) * 18000)
    
    if ((total_kwh_setup_amount / 1000) == 2):
        return 60000
    
    if ((total_kwh_setup_amount / 1000) < 2):
        return (total_kwh_setup_amount / 1000) * 30000
    
def total_overall_cost(type, pincode, total_units_consumed):
    return total_setup_cost(type, pincode, total_units_consumed) + gst(type, pincode, total_units_consumed) - government_subsidy(type, pincode, total_units_consumed)
