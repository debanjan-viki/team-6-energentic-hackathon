import json
import requests
import uuid
import time

# Configuration (reuse your existing config)
bap_id = "bap-ps-network-deg-team1.becknprotocol.io"
bap_uri = "https://bap-ps-network-deg-team1.becknprotocol.io/"
bpp_id = "bpp-ps-network-deg-team1.becknprotocol.io"
bpp_uri = "https://bpp-ps-network-deg-team1.becknprotocol.io/"
bap_endpoint = "https://bap-ps-client-deg-team1.becknprotocol.io"

def confirm_order():
    transaction_id =  "cb0eee6b-8a38-4ef8-8ed2-1f965fcd2e3c"

    item = current_selection["item"]
    provider = current_selection["provider"]

    order = {
        "provider": {"id": provider["id"]},
        "items": [{"id": item["id"], "quantity": {"count": 100}}],
        "billing": {
            "name": "Lisa",
            "phone": "876756454",
            "email": "LisaS@mailinator.com",
            "address": {
                "street": "123 Main St",
                "city": "San Francisco",
                "state": "CA",
                "country": "USA",
                "zip": "94105"
            }
        },
        "fulfillments": [
            {
                "type": "Delivery",
                "end": {
                    "location": {
                        "gps": "37.7749,-122.4194",
                        "address": {
                            "street": "123 Main St",
                            "city": "San Francisco",
                            "state": "CA",
                            "country": "USA",
                            "zip": "94105"
                        }
                    },
                    "contact": {
                        "phone": "876756454",
                        "email": "LisaS@mailinator.com"
                    }
                }
            }
        ],
        "payments": [
            {
                "collected_by": "BPP",
                "params": {
                    "price": "35000",
                    "currency": "USD"
                },
                "type": "PRE-ORDER",
                "status": "PAID"
            }
        ]
    }

    context = {
        "domain": "deg:retail",
        "action": "confirm",
        "version": "1.1.0",
        "bap_id": "bap-ps-network-deg-team1.becknprotocol.io",
        "bap_uri": "https://bap-ps-network-deg-team1.becknprotocol.io/",
        "bpp_id": "bpp-ps-network-deg-team1.becknprotocol.io",
        "bpp_uri": "https://bpp-ps-network-deg-team1.becknprotocol.io/",
        "transaction_id": transaction_id,
        "location": {
            "country": {"code": "USA"},
            "city": {"code": "NANP:628"}
        }
    }

    request_body = {
        "context": context,
        "message": {
            "order": order
        }
    }

    try:
        response = requests.post(bap_endpoint + "/confirm", json=request_body)
        response.raise_for_status()
        response_json = response.json()

        # ✅ Extract confirmation details
        confirmation = response_json["responses"][0]["message"]["order"]
        order_id = confirmation.get("id", "N/A")
        provider_name = confirmation["provider"]["descriptor"].get("name", "N/A")
        item_name = confirmation["items"][0]["descriptor"].get("name", "N/A")
        price = confirmation["quote"]["price"].get("value", "N/A")
        currency = confirmation["quote"]["price"].get("currency", "N/A")

        return f"""✅ Order Confirmed!

🧾 Order ID: {order_id}
🏢 Provider: {provider_name}
📦 Item: {item_name}
💵 Price: {price} {currency}
"""
    except Exception as e:
        return f"❌ Failed to confirm order: {str(e)}\n\nRaw Response:\n{response.text}"

        
result = confirm_order(
    provider_id="104",
    item_id="283"
   
)
print(result)