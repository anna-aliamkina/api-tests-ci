"""
API-тесты для ReqRes, повторяющие логику тестов из Postman

Позитивные:
- test_get_single_user — GET /users/2 - 200, структура и значения
- test_create_user — POST /users - 201, эхо данных + id + createdAt
- test_update_user — PUT /users/2 - 200, обновлённые поля + updatedAt

Негативный:
- test_get_nonexistent_user — GET /users/9999 - 404
"""

import pytest


# ============================================================
# ПОЗИТИВНЫЙ: GET Single User
def test_get_single_user(api_session, base_url):
    """GET /users/2 - 200 OK + корректная структура и данные"""
    response = api_session.get(f"{base_url}/users/2")

    # 1. Статус-код
    assert response.status_code == 200, \
        f"Ожидали 200, получили {response.status_code}"

    # 2. Content-Type — JSON
    assert "application/json" in response.headers.get("Content-Type", ""), \
        "Ответ должен быть в формате JSON"

    # 3. Парсим JSON
    data = response.json()

    # 4. Структура: есть поле data
    assert "data" in data, "В ответе нет поля 'data'"

    user = data["data"]

    # 5. Значения полей
    assert user["id"] == 2, f"Ожидали id=2, получили {user['id']}"
    assert "email" in user, "У пользователя нет email"
    assert "@" in user["email"], "Email должен содержать @"
    assert "first_name" in user, "У пользователя нет first_name"

    print("test_get_single_user: PASSED")


# ============================================================
# ПОЗИТИВНЫЙ: POST Create User
def test_create_user(api_session, base_url):
    """POST /users - 201 Created + эхо данных + id + createdAt"""
    payload = {"name": "Jane", "job": "QA Engineer"}

    response = api_session.post(f"{base_url}/users", json=payload)

    # 1. Статус-код 201
    assert response.status_code == 201, \
        f"Ожидали 201, получили {response.status_code}"

    data = response.json()

    # 2. Эхо переданных полей
    assert data["name"] == "Jane", f"Ожидали name='Jane', получили '{data.get('name')}'"
    assert data["job"] == "QA Engineer"

    # 3. Сервер сгенерировал id и createdAt
    assert "id" in data, "В ответе нет id"
    assert "createdAt" in data, "В ответе нет createdAt"
    assert isinstance(data["id"], str), "id должен быть строкой"

    print("test_create_user: PASSED")


# ============================================================
# ПОЗИТИВНЫЙ: PUT Update User
def test_update_user(api_session, base_url):
    """PUT /users/2 - 200 OK + обновлённые поля + updatedAt"""
    payload = {"name": "Jane Updated", "job": "Senior QA Engineer"}

    response = api_session.put(f"{base_url}/users/2", json=payload)

    # 1. Статус-код 200
    assert response.status_code == 200, \
        f"Ожидали 200, получили {response.status_code}"

    data = response.json()

    # 2. Обновлённые поля
    assert data["name"] == "Jane Updated"
    assert data["job"] == "Senior QA Engineer"

    # 3. Сервер вернул время обновления
    assert "updatedAt" in data, "В ответе нет updatedAt"

    print("test_update_user: PASSED")


# ============================================================
# НЕГАТИВНЫЙ: GET несуществующего пользователя
def test_get_nonexistent_user(api_session, base_url):
    """GET /users/9999 - 404 Not Found"""
    response = api_session.get(f"{base_url}/users/9999")

    # 1. Статус-код 404
    assert response.status_code == 404, \
        f"Ожидали 404, получили {response.status_code}"

    # 2. Тело пустое (для этого mock API)
    assert response.json() == {}, \
        f"Ожидали пустой JSON, получили: {response.json()}"

    print("test_get_nonexistent_user: PASSED")