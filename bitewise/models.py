from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator
import uuid

# Create your models here.
class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

class Budget(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.PROTECT)
    monthlyAmount = models.FloatField(default=0)
    groceryAmount = models.FloatField(default=0)
    otherAmount = models.FloatField(default=0)

class CommitmentCount(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(validators=[MaxValueValidator(7)])
    user = models.ForeignKey(User, on_delete=models.PROTECT)

    @property
    def year(self):
        return self.created_at.year
    
    @property
    def month(self):
        return self.created_at.month

    @property
    def week(self):
        return self.created_at.isocalendar().week
    
class MealCommitment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.TextField(blank=True, null=True, max_length=255)
    cost = models.FloatField(default=0, blank=True)
    achieved = models.DateTimeField(blank=True, null=True)
    activated = models.BooleanField(default= False)
    commitment_count = models.ForeignKey(CommitmentCount, on_delete=models.PROTECT)
