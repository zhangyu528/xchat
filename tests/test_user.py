
def test_register_user_with_password(client):
    response = client.post("/api/register", json={
        "username": "testuser",
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
