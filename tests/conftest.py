import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient


@pytest.fixture
def user():
    user = get_user_model().objects.create_user(
        username='Skywalker',
        email='Anakin.Skywalker@deathstar.com',
        password='padawantomaster',
    )

    return user


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(user, client):
    auth_client = APIClient()
    auth_client.login(username='Skywalker', password='padawantomaster')
    return auth_client
