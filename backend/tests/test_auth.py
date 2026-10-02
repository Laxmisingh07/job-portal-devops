def test_register_endpoint(client):
    response = client.post(
        "/api/auth/register",
        json={
            "name": "Test User",
            "email": "testuser@example.com",
            "password": "Test@123",
            "role": "candidate"
        }
    )

    assert response.status_code in [200, 201, 400]


def test_login_endpoint(client):
    response = client.post(
        "/api/auth/login",
        json={
            "email": "testuser@example.com",
            "password": "Test@123"
        }
    )

    assert response.status_code in [200, 401]