import requests
import uuid
import time
import json
from google.adk.agents import Agent

# Configuration
bap_id = "bap-ps-network-deg-team1.becknprotocol.io"
bap_uri = "https://bap-ps-network-deg-team1.becknprotocol.io/"
bpp_id = "bpp-ps-network-deg-team1.becknprotocol.io"
bpp_uri = "https://bpp-ps-network-deg-team1.becknprotocol.io/"
bap_endpoint = "https://bap-ps-client-deg-team1.becknprotocol.io"

# State
product_map = {}
current_selection = {}

def search_panels():
    global product_map
    product_map = {}  # Reset

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
                        "name": "solar"
                    }
                }
            }
        }
    }

    response = requests.post(bap_endpoint + "/search", json=request_body)

    if response.status_code == 200:
        try:
            data = response.json()
            providers = data["responses"][0]["message"]["catalog"]["providers"]

            formatted_results = "Available Solar Options:\n\n"
            for provider in providers:
                provider_name = provider["descriptor"]["name"]
                provider_id = provider["id"]
                formatted_results += f"Provider: {provider_name} (ID: {provider_id})\n"
                for item in provider.get("items", []):
                    item_name = item["descriptor"]["name"]
                    item_id = item["id"]
                    formatted_results += f"- {item_name} (ID: {item_id})\n"
                    product_map[item_name.lower()] = {
                        "provider_id": provider_id,
                        "item_id": item_id,
                        "provider_name": provider_name,
                        "item_name": item_name
                    }
                formatted_results += "\n"

            return formatted_results.strip()
        except Exception as e:
            return f"Error processing results: {str(e)}"
    else:
        return f"API request failed with status {response.status_code}"


def select_panel(product_name: str):
    global product_map, current_selection
    product = product_map.get(product_name.lower())

    if not product:
        return "Product not found. Please check the name and try again."

    current_selection = {
        "provider_id": product["provider_id"],
        "item_id": product["item_id"],
        "provider_name": product["provider_name"],
        "item_name": product["item_name"]
    }

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
                    "id": product["provider_id"]
                },
                "items": [{
                    "id": product["item_id"]
                }]
            }
        }
    }

    try:
        response = requests.post(bap_endpoint + "/select", json=request_body)
        response.raise_for_status()
        data = response.json()

        order = data['responses'][0]['message']['order']
        provider = order['provider']
        item = order['items'][0]

        result = f"""
Selected Product Details:
------------------------
Provider: {provider['descriptor']['name']} (ID: {product["provider_id"]})
Description: {provider['descriptor'].get('long_desc', 'N/A')}
Rating: {provider.get('rating', 'N/A')}/5

Product: {item['descriptor']['name']} (ID: {product["item_id"]})
Description: {item['descriptor'].get('long_desc', 'N/A')}
Price: {item['price']['value']} {item['price']['currency']}
Available Quantity: {item['quantity']['available']['count']}
Rating: {item.get('rating', 'N/A')}/5
"""
        return result.strip()

    except requests.exceptions.RequestException as e:
        return f"Failed to select product: {str(e)}"
    except (ValueError, KeyError, IndexError) as e:
        return f"Error processing response: {str(e)}"


def init_panel():
    global current_selection

    if not current_selection:
        return "No product has been selected yet. Please select a product first."

    provider_id = current_selection["provider_id"]
    item_id = current_selection["item_id"]

    transaction_id = str(uuid.uuid4())
    current_selection["transaction_id"] = transaction_id

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
            "transaction_id": transaction_id,
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


def confirm_order():
    try:
        transaction_id = current_selection["transaction_id"]
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

        # 🚀 Make the POST request
        response = requests.post(bap_endpoint + "/confirm", json=request_body)

        # ✅ Ensure it was successful
        if response.status_code != 200:
            print(f"❌ Failed to confirm order. Status code: {response.status_code}")
            return

        response_json = response.json()

        # ✅ Safely extract info
        confirmation = response_json.get("responses", [{}])[0].get("message", {}).get("order", {})
        order_id = confirmation.get("id", "Unknown")

        print(f"✅ Order Confirmed! Your Order ID = {order_id}")

    except Exception as e:
        print("❌ Something went wrong:", str(e))

# Agent
root_agent = Agent(
    name="solar_panel_agent",
    description="Solar Panel Search Agent",
    model="gemini-2.0-flash",
    instruction="""
    You are a friendly solar panel assistant. Follow this structured conversation flow:

    1. Greeting:
    Respond politely: "Hello! I'd be happy to help you find solar panel options. Let me check what's available..."

    2. Fetch Solar Panel Options:
    Automatically call search_panels().

    3. Present the Results in This Format:
    "Here are the available solar options:\n\n"
    "Provider: [Provider Name]\n"
    "- [Product Name] (ID: [Item ID])"

    4. Prompt for User Selection:
    Ask:
    "Would you like more details about any of these products? Please tell me the exact product name you're interested in."

    5. When the User Provides a Product Name:
    - Call select_panel(product_name).
    - Display the detailed response.
    - Ask: "Would you like to initialize an order for this product?"
    - If the user says yes:
      - Call init_panel().
      - Display the init order details.
      - Then ask: "Would you like to confirm this order?"
      - If the user says yes, call confirm_order() using the stored current_selection.
    - Otherwise, continue the conversation accordingly.

    6. If the Product Name is Not Found:
    Respond:
    "I couldn't find that exact product. Would you like to see the options again or try a different product name?"

    Tone:
    Always maintain a helpful, professional, and friendly tone.
    """,
    tools=[search_panels, select_panel, init_panel, confirm_order]
)
