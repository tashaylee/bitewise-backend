import pytest
from budget.models import Budget
from shared.models import User


# TO DO: setup mock tests + create test data file

budget_data = {
    'monthlyAmount': 300,
    'groceryAmount': 55
}

@pytest.fixture
def budget(user, db):
    return Budget.objects.create(user=user, **budget_data)

@pytest.mark.django_db
class TestBudget:
    def test_post_budget(self, auth_client):
        response = auth_client.post('/api/budgets/', data=budget_data)
        assert response.status_code == 200
        assert len(response.data) != 0

    def test_get_budgets(self, auth_client, budget_1):
        response = auth_client.get('/api/budgets/')
        assert response.status_code == 200
        assert len(response.data) == 1