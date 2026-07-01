def test_register_rate_limit(client):
    for index in range(5):
        response = client.post(
            "/api/v1/auth/register",
            json={
                "email": f"rate{index}@test.com",
                "password": "password123",
                "dni": f"9999999{index}X"
            }
        )

        assert response.status_code == 201

    blocked_response = client.post(
        "/api/v1/auth/register",
        json={
            "email": "blocked@test.com",
            "password": "password123",
            "dni": "99999999X"
        }
    )

    assert blocked_response.status_code == 429


def test_login_rate_limit(client):
    for _ in range(10):
        response = client.post(
            "/api/v1/auth/login",
            data={
                "username": "unknown@test.com",
                "password": "wrong-password"
            }
        )

        assert response.status_code == 401

    blocked_response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "unknown@test.com",
            "password": "wrong-password"
        }
    )

    assert blocked_response.status_code == 429