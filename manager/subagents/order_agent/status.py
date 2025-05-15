import json
import requests
import uuid
import time

# Configuration (same as your select_panel function)
bap_id = "bap-ps-network-deg-team1.becknprotocol.io"
bap_uri = "https://bap-ps-network-deg-team1.becknprotocol.io/"
bpp_id = "bpp-ps-network-deg-team1.becknprotocol.io"
bpp_uri = "https://bpp-ps-network-deg-team1.becknprotocol.io/"
bap_endpoint = "https://bap-ps-client-deg-team1.becknprotocol.io"

def check_order_status(order_id):
    """
    Checks the status of a specific order
    Args:
        order_id: ID of the order to check status for
    Returns:
        Formatted response with order status details or error message
    """
    request_body = {
        "context": {
            "domain": "deg:retail",
            "action": "status",
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
            "order_id": order_id
        }
    }

    try:
        response = requests.post(bap_endpoint + "/status", json=request_body)
        response.raise_for_status()
        data = response.json()
        
        # Extract relevant information from the response
        order = data['responses'][0]['message']['order']
        provider = order['provider']
        items = order['items']
        quote = order['quote']
        fulfillments = order['fulfillments'][0]
        payment = order['payment']
        
        # Format the response
        result = f"""
Order Status Details:
--------------------
Order ID: {order_id}
Status: {order['state']}

Provider: {provider['descriptor']['name']}
Description: {provider['descriptor']['long_desc']}

Items:
"""
        for item in items:
            result += f"- {item['descriptor']['name']} (Qty: {item['quantity']['selected']['count']})\n"
        
        result += f"""
Pricing:
- Total: {quote['price']['value']} {quote['price']['currency']}
- Payment Status: {payment['status']}
- Payment Method: {payment['type']}

Delivery:
- Status: {fulfillments['state']}
- Type: {fulfillments['type']}
- Tracking: {fulfillments.get('tracking', 'Not available')}
- Estimated Delivery: {fulfillments.get('end', {}).get('time', {}).get('timestamp', 'Not specified')}
"""
        return result.strip()
        
    except requests.exceptions.RequestException as e:
        return f"Failed to check order status: {str(e)}"
    except (ValueError, KeyError, IndexError) as e:
        return f"Error processing response: {str(e)}"

# Example usage
result = check_order_status(order_id="3782")
print(result)