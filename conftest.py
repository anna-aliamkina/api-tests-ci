"""Общие настройки и фикстуры для тестов API ReqRes"""

import pytest
import requests

BASE_URL = "https://reqres.in/api"


@pytest.fixture(scope="session")
def api_session():
    """
    Одна HTTP-сессия на все тесты
    Сессия переиспользует TCP-соединение — тесты работают быстрее
    """
    session = requests.Session()
    # Заголовок Accept — просим сервер вернуть JSON
    session.headers.update({"Accept": "application/json"})
    yield session
    session.close()


@pytest.fixture
def base_url():
    return BASE_URL