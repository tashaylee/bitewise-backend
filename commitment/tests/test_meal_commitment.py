import pytest
from commitment.models import *


meal_commitment_data = {
    'name':'chicken and waffles',
    'cost': 20.50,
}

# TO DO: setup mock tests + create test data file
@pytest.mark.django_db
class TestMealCommitment:
    def test_get_meal_commitments(self, auth_client, commitment_count_1):
        response = auth_client.get('/api/mealcommitments/')
        assert response.status_code == 200
        assert len(response.data) > 0
    
    def test_get_incomplete_meal_commitments(self, auth_client, commitment_count_1):
        response = auth_client.get('/api/mealcommitments/incomplete/')
        assert response.status_code == 200
        assert len(response.data) == 2

    def test_put_meal_commitment(self, auth_client, commitment_count_1):
        incomplete_meal_commitments = auth_client.get('/api/mealcommitments/incomplete/').data

        for incomplete in incomplete_meal_commitments:
            pk = incomplete.get('id')
            
            response = auth_client.put(f'/api/mealcommitments/{pk}/', data=meal_commitment_data)
            assert response.status_code == 200
            assert response.data.get('meal_commitment_id')
