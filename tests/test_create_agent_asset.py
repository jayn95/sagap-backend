import requests
from datetime import datetime

BASE_URL = "http://127.0.0.1:8000"


# ==========================
# AGENT TEST FUNCTIONS
# ==========================
def create_agent():
    payload = {
        "employee_no": "EMP100",
        "full_name": "Jane Doe",
        "designation": "Developer",
        "department": "IT",
        "contact_number": "+639123456789",
        "email": "jane.doe@test.com",
        "current_address": "123 Test St, Test City",
        "status": "Active"
    }

    response = requests.post(f"{BASE_URL}/agents/", json=payload)

    if response.status_code == 200:
        agent = response.json()
        print("\n✅ Agent created successfully:")
        print(agent)
        return agent["agent_id"]
    else:
        print("\n❌ Failed to create agent")
        print(response.status_code)
        print(response.text)
        return None


def get_all_agents():
    response = requests.get(f"{BASE_URL}/agents/")
    if response.status_code == 200:
        print("\n📋 All agents:")
        for agent in response.json():
            print(agent)
    else:
        print("\n❌ Failed to get agents")


def get_agent_by_id(agent_id):
    response = requests.get(f"{BASE_URL}/agents/{agent_id}")
    if response.status_code == 200:
        print("\n🔎 Agent found:")
        print(response.json())
    else:
        print("\n❌ Agent not found")


def delete_agent(agent_id):
    response = requests.delete(f"{BASE_URL}/agents/{agent_id}")
    if response.status_code == 200:
        print("\n🗑️ Agent deleted successfully")
    else:
        print("\n❌ Failed to delete agent")


# ==========================
# ASSET TEST FUNCTIONS
# ==========================
def create_asset():
    payload = {
        "asset_type": "Desktop",
        "asset_tag": "AST100",
        "serial_number": "SN-123456",
        "serial_number_2": None,
        "brand": "Dell",
        "model": "OptiPlex 7000",
        "memory": "16GB",
        "quantity": 1,
        "condition": "New",
        "status": "Available",
        "created_at": str(datetime.utcnow())
    }

    response = requests.post(f"{BASE_URL}/assets/", json=payload)

    if response.status_code == 200:
        asset = response.json()
        print("\n✅ Asset created successfully:")
        print(asset)
        return asset["asset_id"]
    else:
        print("\n❌ Failed to create asset")
        print(response.status_code)
        print(response.text)
        return None


def get_all_assets():
    response = requests.get(f"{BASE_URL}/assets/")
    if response.status_code == 200:
        print("\n📋 All assets:")
        for asset in response.json():
            print(asset)
    else:
        print("\n❌ Failed to get assets")


def get_asset_by_id(asset_id):
    response = requests.get(f"{BASE_URL}/assets/{asset_id}")
    if response.status_code == 200:
        print("\n🔎 Asset found:")
        print(response.json())
    else:
        print("\n❌ Asset not found")


def delete_asset(asset_id):
    response = requests.delete(f"{BASE_URL}/assets/{asset_id}")
    if response.status_code == 200:
        print("\n🗑️ Asset deleted successfully")
    else:
        print("\n❌ Failed to delete asset")


# ==========================
# MAIN TEST RUNNER
# ==========================
def main():
    print("\n==============================")
    print(" AGENT TESTS ")
    print("==============================")
    agent_id = create_agent()
    if agent_id:
        get_all_agents()
        get_agent_by_id(agent_id)
        delete_agent(agent_id)

    print("\n==============================")
    print(" ASSET TESTS ")
    print("==============================")
    asset_id = create_asset()
    if asset_id:
        get_all_assets()
        get_asset_by_id(asset_id)
        delete_asset(asset_id)

    print("\n==============================")
    print(" TEST COMPLETE ")
    print("==============================")


if __name__ == "__main__":
    main()
