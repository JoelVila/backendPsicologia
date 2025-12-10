import requests
import json
import time

# Docker maps port 5000 to 5000
BASE_URL = "http://127.0.0.1:5000"

def verify_main_auth():
    print("Verifying Auth in Main Routes (Docker version)...")
    
    # Wait loop to ensure server is up (useful if user just ran docker-compose up)
    for i in range(5):
        try:
            requests.get(BASE_URL)
            break
        except requests.exceptions.ConnectionError:
            print(f"Waiting for server... ({i+1}/5)")
            time.sleep(2)

    # 1. Register
    register_url = f"{BASE_URL}/register_paciente"
    user_data = {
        "nombre": "DockerUser",
        "email": "docker_test@example.com",
        "password": "dockerpassword",
        "apellido": "Container",
        "edad": 99,
        "telefono": "987654321",
        "tipo_paciente": "test",
        "tipo_tarjeta": "mastercard"
    }
    
    print(f"1. Registering user at {register_url}...")
    try:
        response = requests.post(register_url, json=user_data)
        if response.status_code == 201:
            print("   SUCCESS: User registered.")
        elif response.status_code == 400 and "Email already exists" in response.text:
            print("   NOTE: User already exists, proceeding to login.")
        else:
            print(f"   FAILURE: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return

    # 2. Login
    login_url = f"{BASE_URL}/login_paciente"
    login_data = {"email": "docker_test@example.com", "password": "dockerpassword"}
    
    print(f"2. Logging in at {login_url}...")
    token = None
    try:
        response = requests.post(login_url, json=login_data)
        if response.status_code == 200:
            token = response.json().get('access_token')
            print("   SUCCESS: Logged in.")
        else:
            print(f"   FAILURE: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"   ERROR: {e}")
        return

    # 3. Profile
    profile_url = f"{BASE_URL}/perfil_paciente"
    headers = {"Authorization": f"Bearer {token}"}
    
    print(f"3. Getting profile at {profile_url}...")
    try:
        response = requests.get(profile_url, headers=headers)
        if response.status_code == 200:
            print(f"   SUCCESS: Profile retrieved: {response.json()}")
        else:
            print(f"   FAILURE: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"   ERROR: {e}")

if __name__ == "__main__":
    verify_main_auth()
