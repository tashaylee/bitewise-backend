import pytest
from shared.models import User

@pytest.mark.django_db
class TestUser:
    def test_create_user(self, user):
        assert User.objects.count() == 1