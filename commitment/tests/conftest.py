import pytest
from commitment.models import *

@pytest.fixture
def commitment_count_1(db, user):
    return CommitmentCount.objects.create(
        user=user,
        count = 2
    )
