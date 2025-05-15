import json
import requests
import uuid
import time

# Configuration
bap_id = "bap-ps-network-deg-team1.becknprotocol.io"
bap_uri = "https://bap-ps-network-deg-team1.becknprotocol.io/"
bpp_id = "bpp-ps-network-deg-team1.becknprotocol.io"
bpp_uri = "https://bpp-ps-network-deg-team1.becknprotocol.io/"
bap_endpoint = "https://bap-ps-client-deg-team1.becknprotocol.io"

def select_panel(provider_id, item_id):
    """
    Selects a specific solar panel from a provider
    Args:
        provider_id: ID of the provider (from search results)
        item_id: ID of the solar panel item (from search results)
    Returns:
        Formatted response with product details or error message
    """
    request_body = {
        "context": {
            "domain": "deg:retail",
            "action": "select",
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
            "order": {
                "provider": {
                    "id": provider_id
                },
                "items": [{
                    "id": item_id
                }]
            }
        }
    }

    try:
        response = requests.post(bap_endpoint + "/select", json=request_body)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information from the response
        order = data['responses'][0]['message']['order']
        provider = order['provider']
        item = order['items'][0]
        quote = order['quote']
        
        # Format the response
        result = f"""
Selected Product Details:
------------------------
Provider: {provider['descriptor']['name']} ({provider_id})
Description: {provider['descriptor']['long_desc']}
Rating: {provider['rating']}/5

Product: {item['descriptor']['name']} ({item_id})
Description: {item['descriptor']['long_desc']}
Price: {item['price']['value']} {item['price']['currency']}
Available Quantity: {item['quantity']['available']['count']}
Rating: {item['rating']}/5

Pricing Breakdown:
- Base Price: {quote['breakup'][0]['price']['value']} {quote['breakup'][0]['price']['currency']}
- Tax: {quote['breakup'][1]['price']['value']} {quote['breakup'][1]['price']['currency']}
- Delivery: {quote['breakup'][2]['price']['value']} {quote['breakup'][2]['price']['currency']}
Total: {quote['price']['value']} {quote['price']['currency']}

Delivery: {order['fulfillments'][0]['type']}
Estimated Rating: {order['fulfillments'][0]['rating']}/5
"""
        return result.strip()
        
    except requests.exceptions.RequestException as e:
        return f"Failed to select panel: {str(e)}"
    except (ValueError, KeyError, IndexError) as e:
        return f"Error processing response: {str(e)}"

# Example usage with the IDs from your response
result = select_panel(provider_id="104", item_id="283")
print(result)