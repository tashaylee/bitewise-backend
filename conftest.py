import pytest
from rest_framework.test import APIClient
from budget.models import Budget
from shared.models import User
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def api_client() -> APIClient:
    return APIClient()

@pytest.fixture
def user():
    user = User.objects.create_user(
        first_name="dwayne",
        last_name="johnson",
        email="dwaynetherock@johnson.com",
        username="dwayne johnson",
    )
    return user


@pytest.fixture
def access_token(user):
    refresh = str(AccessToken.for_user(user))
    return refresh

@pytest.fixture
def auth_client(api_client, access_token):
    client = api_client
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return client
