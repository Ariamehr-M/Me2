import requests
import uuid

BASE_URL = "http://localhost:8000"

# Helper to print step headers
def step(msg):
    print(f"\n{'='*10} {msg} {'='*10}")

# Generate unique emails for each run
user_a_email = f"usera_{uuid.uuid4().hex[:8]}@example.com"
user_b_email = f"userb_{uuid.uuid4().hex[:8]}@example.com"

# 1. Register User A
step("Register User A")
user_a = {"email": user_a_email, "password": "passwordA", "name": "Alice"}
r = requests.post(f"{BASE_URL}/auth/register", json=user_a)
assert r.status_code == 200, r.text
user_a_id = r.json()["id"]
print("User A ID:", user_a_id)

# 2. Login User A
step("Login User A")
r = requests.post(f"{BASE_URL}/auth/login", data={"username": user_a["email"], "password": user_a["password"]})
assert r.status_code == 200, r.text
token_a = r.json()["access_token"]
headers_a = {"Authorization": f"Bearer {token_a}"}
print("User A Token:", token_a)

# 3. User A creates a pair
step("User A creates a pair")
pair_data = {"user_a_id": user_a_id}
r = requests.post(f"{BASE_URL}/pairs/", json=pair_data, headers=headers_a)
assert r.status_code == 200, r.text
pair = r.json()
pair_id = pair["id"]
invite_token = pair["invite_token"]
print("Pair ID:", pair_id, "Invite Token:", invite_token)

# 4. User A fetches questions
step("User A fetches questions")
r = requests.get(f"{BASE_URL}/questions/", headers=headers_a)
assert r.status_code == 200, r.text
questions = r.json()
print(f"Fetched {len(questions)} questions.")

# 5. User A fetches options for each question and submits responses
step("User A submits responses")
for q in questions:
    qid = q["id"]
    r_opt = requests.get(f"{BASE_URL}/questions/{qid}/options", headers=headers_a)
    assert r_opt.status_code == 200, r_opt.text
    options = r_opt.json()
    if not options:
        continue  # skip if no options
    option_id = options[0]["id"]  # pick first option for test
    response = {
        "pair_id": pair_id,
        "respondent_id": user_a_id,
        "question_id": qid,
        "option_id": option_id
    }
    r_resp = requests.post(f"{BASE_URL}/responses/", json=response, headers=headers_a)
    assert r_resp.status_code == 200, r_resp.text
print("User A responses submitted.")

# 6. User A gets the invite link
step("User A gets invite link")
r = requests.get(f"{BASE_URL}/pairs/invite/{invite_token}", headers=headers_a)
assert r.status_code == 200, r.text
print("Invite link info:", r.json())

# 7. Register User B
step("Register User B")
user_b = {"email": user_b_email, "password": "passwordB", "name": "Bob"}
r = requests.post(f"{BASE_URL}/auth/register", json=user_b)
assert r.status_code == 200, r.text
user_b_id = r.json()["id"]
print("User B ID:", user_b_id)

# 8. Login User B
step("Login User B")
r = requests.post(f"{BASE_URL}/auth/login", data={"username": user_b["email"], "password": user_b["password"]})
assert r.status_code == 200, r.text
token_b = r.json()["access_token"]
headers_b = {"Authorization": f"Bearer {token_b}"}
print("User B Token:", token_b)

# 9. User B opens invite link
step("User B opens invite link")
r = requests.get(f"{BASE_URL}/pairs/invite/{invite_token}", headers=headers_b)
assert r.status_code == 200, r.text
print("Invite link info for User B:", r.json())

# 10. User B accepts invite
step("User B accepts invite")
r = requests.post(f"{BASE_URL}/pairs/invite/{invite_token}/accept", headers=headers_b)
assert r.status_code == 200, r.text
print("Pair after User B accepted:", r.json())

# 11. User B fetches questions and submits responses
step("User B submits responses")
r = requests.get(f"{BASE_URL}/questions/", headers=headers_b)
assert r.status_code == 200, r.text
questions = r.json()
for q in questions:
    qid = q["id"]
    r_opt = requests.get(f"{BASE_URL}/questions/{qid}/options", headers=headers_b)
    assert r_opt.status_code == 200, r_opt.text
    options = r_opt.json()
    if not options:
        continue
    option_id = options[0]["id"]  # pick first option for test
    response = {
        "pair_id": pair_id,
        "respondent_id": user_b_id,
        "question_id": qid,
        "option_id": option_id
    }
    r_resp = requests.post(f"{BASE_URL}/responses/", json=response, headers=headers_b)
    assert r_resp.status_code == 200, r_resp.text
print("User B responses submitted.")

# 12. Fetch overlap results
step("Fetch overlap results")
r = requests.get(f"{BASE_URL}/responses/pair/{pair_id}/overlap", headers=headers_a)
assert r.status_code == 200, r.text
print("Overlap results:", r.json()) 