import requests
import json

BASE_URL = "http://localhost:8000"

def test_create_room():
    """Test room creation endpoint"""
    response = requests.post(f"{BASE_URL}/rooms/", json={})
    print(f"Create Room Response: {response.status_code}")
    print(f"Room Data: {response.json()}")
    return response.json().get("roomId")

def test_autocomplete():
    """Test autocomplete endpoint"""
    data = {
        "code": "def hello",
        "cursorPosition": 9,
        "language": "python"
    }
    response = requests.post(f"{BASE_URL}/autocomplete", json=data)
    print(f"Autocomplete Response: {response.status_code}")
    print(f"Suggestion: {response.json()}")

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/")
    print(f"Health Check: {response.status_code}")
    print(f"Message: {response.json()}")

if __name__ == "__main__":
    print("Testing CodeSync API...")
    print("=" * 40)
    
    test_health()
    print()
    
    room_id = test_create_room()
    print()
    
    test_autocomplete()
    print()
    
    print(f"WebSocket URL: ws://localhost:8000/ws/{room_id}")
    print("=" * 40)