from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Budget(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    monthlyAmount = models.FloatField()
    groceryAmount = models.DecimalField(max_digits = 5,
                                        decimal_places = 2,
                                        blank = True)
    otherAmount = models.DecimalField(max_digits = 5,
                                        decimal_places = 2,
                                        blank = True)

class CommitmentCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    year = models.IntegerField()
    month = models.IntegerField()
    week = models.IntegerField()
    count = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.PROTECT)
