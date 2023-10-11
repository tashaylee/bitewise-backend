from django.db import models
from ..models import User

class Budget(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    monthlyAmount = models.FloatField(default=0)
    groceryAmount = models.FloatField(default=0)
    otherAmount = models.FloatField(default=0)
