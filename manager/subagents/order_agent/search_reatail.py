import requests
import uuid
import time

# Replace these with your actual Beckn network values
bap_id = "bap-ps-network-deg-team1.becknprotocol.io"
bap_uri = "https://bap-ps-network-deg-team1.becknprotocol.io/"
bpp_id = "bpp-ps-network-deg-team1.becknprotocol.io"
bpp_uri = "https://bpp-ps-network-deg-team1.becknprotocol.io/"
bap_endpoint = "https://bap-ps-client-deg-team1.becknprotocol.io"  # your BAP client endpoint

# Map product names to IDs
product_map = {}

def search_panels(search_term="solar"):
    global product_map
    product_map = {}  # reset

    request_body = {
        "context": {
            "domain": "deg:retail",
            "action": "search",
            "location": {
                "country": {"code": "USA"},
                "city": {"code": "NANP:628"}
            },
            "version": "1.1.0",
            "bap_id": bap_id,
            "bap_uri": bap_uri,
            "bpp_id": bpp_id,
            "bpp_uri": bpp_uri,
            "transaction_id": str(uuid.uuid4()),
            "message_id": str(uuid.uuid4()),
            "timestamp": str(int(time.time()))
        },
        "message": {
            "intent": {
                "item": {
                    "descriptor": {
                        "name": search_term
                    }
                }
            }
        }
    }

    response = requests.post(bap_endpoint + "/search", json=request_body)

    if response.status_code == 200:
        try:
            data = response.json()
            responses = data.get("responses", [])

            if not responses:
                return "No responses found in API response."

            formatted_results = "Available Solar Options:\n\n"
            for resp in responses:
                message = resp.get("message", {})
                catalog = message.get("catalog", {})
                providers = catalog.get("providers", [])

                for provider in providers:
                    provider_name = provider.get("descriptor", {}).get("name", "Unknown Provider")
                    provider_id = provider.get("id", "N/A")
                    formatted_results += f"Provider: {provider_name} (ID: {provider_id})\n"
                    for item in provider.get("items", []):
                        item_name = item.get("descriptor", {}).get("name", "Unnamed Item")
                        item_id = item.get("id", "N/A")
                        formatted_results += f"- {item_name} (ID: {item_id})\n"
                        # Save to product map
                        product_map[item_name.lower()] = {
                            "provider_id": provider_id,
                            "item_id": item_id
                        }
                    formatted_results += "\n"

            return formatted_results.strip()
        except Exception as e:
            return f"Error processing results: {str(e)}"
    else:
        return f"API request failed with status {response.status_code} - {response.text}"




print(search_panels())
