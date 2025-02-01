import requests

BASE_URL = "http://127.0.0.1:8000/api"

ENDPOINTS = {
    "register": f"{BASE_URL}/user/register/",
    "login": f"{BASE_URL}/user/login/",
    "users": f"{BASE_URL}/chat/users/",
    "send_message": f"{BASE_URL}/chat/messages/send/",
    "unread_messages": f"{BASE_URL}/chat/messages/unread/",
    "chat_history": f"{BASE_URL}/chat/messages/",  # Append receiver ID when needed
}

HEADERS = {"Content-Type": "application/json"}


# ✅ Function to register a user
def register_user(username, email, password, profile_pic=None):
    data = {
        "username": username,
        "email": email,
        "password": password,
    }
    if profile_pic:
        data["profile_picture"] = profile_pic

    response = requests.post(ENDPOINTS["register"], json=data, headers=HEADERS)
    print(f"REGISTER {username}: {response.status_code}, {response.json()}")
    return response.text


# ✅ Function to log in
def login_user(username, password):
    data = {"username": username, "password": password}
    response = requests.post(ENDPOINTS["login"], json=data, headers=HEADERS)
    if response.status_code == 200:
        token = response.json().get("access")
        print(f"LOGIN {username}: {response.status_code}, Token: {token}")
        return token
    else:
        print(f"LOGIN ERROR: {response.status_code}, {response.json()}")
        return None


# ✅ Function to fetch all users (contacts)
def fetch_users(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["users"], headers=headers)
    print(f"USERS LIST: {response.status_code}, {response.json()}")


# ✅ Function to send a message
def send_message(token, receiver_id, message):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"receiver_id": receiver_id, "message": message}
    response = requests.post(ENDPOINTS["send_message"], json=data, headers=headers)
    print(f"SEND MESSAGE: {response.status_code}, {response.json()}")


# ✅ Function to fetch unread messages
def fetch_unread_messages(token):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(ENDPOINTS["unread_messages"], headers=headers)
    print(f"UNREAD MESSAGES: {response.status_code}, {response.json()}")


# ✅ Function to fetch chat history with a specific user
def fetch_chat_history(token, receiver_id):
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(
        f"{ENDPOINTS['chat_history']}{receiver_id}/", headers=headers
    )
    print(f"CHAT HISTORY: {response.status_code}, {response.json()}")


# 🔥 Run API Tests
if __name__ == "__main__":
    print("🚀 Starting API Test...\n")

    # Step 1: Register Two Users
    register_user(
        "testuser1",
        "testuser1@example.com",
        "password123",
        "default_profile_pics/3.png",
    )
    register_user("testuser2", "testuser2@example.com", "password123")

    # Step 2: Login and Get Tokens
    token1 = login_user("testuser1", "password123")
    token2 = login_user("testuser2", "password123")

    if not token1 or not token2:
        print("❌ Login Failed. Fix authentication first.")
        exit()

    # Step 3: Fetch Users
    fetch_users(token1)

    # Step 4: Send a Message from testuser1 to testuser2
    send_message(token1, 2, "Hello testuser2! This is testuser1.")

    # Step 5: testuser2 checks unread messages
    fetch_unread_messages(token2)

    # Step 6: Fetch chat history between the users
    fetch_chat_history(token2, 1)

    print("\n✅ API Test Completed!")
