import requests
import os
from dotenv import load_dotenv
load_dotenv()


class Enrollment:
    def __init__(self):
        self.base_url = os.getenv("BASE_URL")
        if not self.base_url:
            raise EnvironmentError("BASE_URL environment variable not set")
 
    def create_and_toggle_der(self, energy_resource_id, appliance_id=13):
        # Step 1: Call Create DER API
        for i in range(4):
            create_url = f"{self.base_url}/der"
            create_payload = {
                "energy_resource": energy_resource_id,
                "appliance": appliance_id
            }
            create_response = requests.post(create_url, json=create_payload)
            # create_response.raise_for_status()
       
            der_data = create_response.json()
            print(der_data)
            der_id = der_data.get("id")  # Adjust key based on actual API response
 
            if not der_id:
                raise ValueError("DER ID not found in create response")
 
        # Step 2: Call Toggle DER Switching API
            toggle_url = f"{self.base_url}/toggle-der/{energy_resource_id}"
            toggle_payload = {
                "der_id": der_id,
                "switched_on": True
            }
            toggle_response = requests.post(toggle_url, json=toggle_payload)
            toggle_response.raise_for_status()
 
        response = toggle_response.json()
        return response.get("message")  # Adjust key based on actual API response