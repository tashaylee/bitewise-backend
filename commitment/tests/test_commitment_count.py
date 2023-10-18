import pytest
from commitment.models import *

# TO DO: setup mock tests + create test data file
commitment_count_data = {
    'count': 3,
}

@pytest.mark.django_db
class TestCommitmentCount:
    def test_post_commitment_count(self, auth_client):
        response = auth_client.post('/api/commitmentcounts/', data=commitment_count_data)
        assert response.status_code == 200
        assert response.data.get('commitment_count_id')

    def test_get_commitment_count(self, auth_client, commitment_count_1):
        response = auth_client.get('/api/commitmentcounts/')
        assert response.status_code == 200
        assert len(response.data) > 0