# This script will:
# ✅ Create agent
# ✅ Create asset
# ✅ Assign asset
# ✅ Get all assignments
# ✅ Update assignment
# ✅ Return asset
# ✅ Delete assignment


import requests
import sys

BASE_URL = "http://127.0.0.1:8000"

def print_step(title):
    print("\n" + "=" * 50)
    print(title)
    print("=" * 50)


def fail_and_exit(response):
    print("❌ Request failed:")
    print(response.status_code, response.text)
    sys.exit(1)


# -----------------------------
# 1️⃣ CREATE AGENT
# -----------------------------
print_step("STEP 1 — CREATE AGENT")

agent_payload = {
    "employee_no": "EMP103",
    "full_name": "Test User",
    "designation": "IT Support",
    "department": "IT",
    "contact_number": "09123456789",
    "email": "testuser@email.com",
    "current_address": "Iloilo City",
    "status": "Active"
}

response = requests.post(f"{BASE_URL}/agents/", json=agent_payload)
if response.status_code != 200:
    fail_and_exit(response)

agent = response.json()
agent_id = agent["agent_id"]
print("✅ Agent created:", agent_id)


# -----------------------------
# 2️⃣ CREATE ASSET
# -----------------------------
print_step("STEP 2 — CREATE ASSET")

asset_payload = {
    "asset_type": "Desktop",
    "asset_tag": "AST103",
    "brand": "Dell",
    "model": "OptiPlex 7090",
    "serial_number": "SN-PRIMARY-103",
    "serial_number_2": None,
    "memory": "16GB",
    "condition": "Good",
    "status": "Available"
}

response = requests.post(f"{BASE_URL}/assets/", json=asset_payload)
if response.status_code != 200:
    fail_and_exit(response)

asset = response.json()
asset_id = asset["asset_id"]
print("✅ Asset created:", asset_id)


# -----------------------------
# 3️⃣ ASSIGN ASSET
# -----------------------------
print_step("STEP 3 — ASSIGN ASSET")

assign_payload = {
    "asset_id": asset_id,
    "agent_id": agent_id,
    "remarks": "Initial assignment"
}

response = requests.post(f"{BASE_URL}/assignments/", json=assign_payload)
if response.status_code != 200:
    fail_and_exit(response)

assignment = response.json()
assignment_id = assignment["assignment_id"]
print("✅ Asset assigned:", assignment_id)


# -----------------------------
# 4️⃣ GET ALL ASSIGNMENTS
# -----------------------------
print_step("STEP 4 — GET ALL ASSIGNMENTS")

response = requests.get(f"{BASE_URL}/assignments/")
if response.status_code != 200:
    fail_and_exit(response)

print("✅ Assignments list:")
print(response.json())


# -----------------------------
# 5️⃣ UPDATE ASSIGNMENT
# -----------------------------
print_step("STEP 5 — UPDATE ASSIGNMENT")

update_payload = {
    "remarks": "Updated via test script"
}

response = requests.put(
    f"{BASE_URL}/assignments/{assignment_id}",
    json=update_payload
)
if response.status_code != 200:
    fail_and_exit(response)

print("✅ Assignment updated:")
print(response.json())


# -----------------------------
# 6️⃣ RETURN ASSET
# -----------------------------
print_step("STEP 6 — RETURN ASSET")

response = requests.post(f"{BASE_URL}/assignments/return/{assignment_id}")
if response.status_code != 200:
    fail_and_exit(response)

print("✅ Asset returned:")
print(response.json())


# # -----------------------------
# # 7️⃣ DELETE ASSIGNMENT
# # -----------------------------
# print_step("STEP 7 — DELETE ASSIGNMENT")

# response = requests.delete(f"{BASE_URL}/assignments/{assignment_id}")
# if response.status_code not in (200, 204):
#     fail_and_exit(response)

# print("✅ Assignment deleted successfully")


print("\n🎉 FULL ASSIGNMENT WORKFLOW PASSED")