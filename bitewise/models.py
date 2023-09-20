from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.

class Budget(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    monthlyAmount = models.FloatField()
    groceryAmount = models.DecimalField(max_digits = 5,
                                        decimal_places = 2,
                                        blank = True)
    otherAmount = models.DecimalField(max_digits = 5,
                                        decimal_places = 2,
                                        blank = True)
    

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    budget = models.OneToOneField(Budget, on_delete=models.PROTECT, blank=True, null=True)


class CommitmentCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
