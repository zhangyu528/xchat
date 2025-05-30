
def test_register_user_with_password(client):
    response = client.post("/api/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_login_user(client):
    # 创建用户
    client.post("/api/register", json={
        "email": "test@example.com",
        "password": "password123",
    })
    # 登录用户
    response = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()