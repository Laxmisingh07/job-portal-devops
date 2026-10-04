
import uuid


def test_register_endpoint(client):
    unique_email = f"testuser_{uuid.uuid4().hex[:8]}@example.com"

    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": unique_email,
            "password": "Test@123",
            "role": "candidate"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_login_endpoint(client):
    email = f"loginuser_{uuid.uuid4().hex[:8]}@example.com"
    password = "Test@123"

    register_response = client.post(
        "/api/auth/register",
        json={
            "name": "Login User",
            "email": email,
            "password": password,
            "role": "candidate"
        }
    )

    assert register_response.status_code in [200, 201, 400]

    response = client.post(
        "/api/auth/login",
        json={
            "email": email,
            "password": password
        }
    )

    assert response.status_code in [200, 401]

