
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


def test_get_me(client):
    # 1. 注册并登录，获取 access_token
    client.post("/api/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    login_resp = client.post("/api/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert login_resp.status_code == 200
    access_token = login_resp.json()["access_token"]

    # 2. 用 token 访问 /me
    headers = {"Authorization": f"Bearer {access_token}"}
    me_resp = client.get("/api/me", headers=headers)
    assert me_resp.status_code == 200
    data = me_resp.json()
    assert data["email"] == "test@example.com"
    assert "id" in data