import pytest

@pytest.mark.django_db
class TestIngredients:
    def test_create_ingredient(self, user, store_1, api_client):
        pass