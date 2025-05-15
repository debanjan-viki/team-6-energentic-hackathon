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

def init_panel(provider_id, item_id):
    """
    Initialize an order for a specific solar panel item from a provider.
    Args:
        provider_id: ID of the provider (string)
        item_id: ID of the item (string)
    Returns:
        Formatted string of init response or error message
    """
    request_body = {
        "context": {
            "domain": "deg:retail",
            "action": "init",
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
                "items": [
                    {
                        "id": item_id
                    }
                ]
            }
        }
    }

    try:
        response = requests.post(bap_endpoint + "/init", json=request_body)
        response.raise_for_status()
        data = response.json()

        # Extract relevant info — adjust keys according to actual API response
        order = data['responses'][0]['message']['order']
        provider = order['provider']
        item = order['items'][0]

        result = f"""
Init Order Details:
-------------------
Provider: {provider['descriptor']['name']} ({provider_id})
Description: {provider['descriptor'].get('long_desc', 'N/A')}

Product: {item['descriptor']['name']} ({item_id})
Description: {item['descriptor'].get('long_desc', 'N/A')}
Price: {item['price']['value']} {item['price']['currency']}
Available Quantity: {item['quantity']['available']['count']}
"""
        return result.strip()

    except requests.exceptions.RequestException as e:
        return f"Failed to init panel: {str(e)}"
    except (ValueError, KeyError, IndexError) as e:
        return f"Error processing response: {str(e)}"


# Example usage with provider and item IDs
result = init_panel(provider_id="27", item_id="33")
print(result)
