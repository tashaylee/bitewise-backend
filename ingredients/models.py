from django.db import models
from shared.models import User
from store.models import Store


class Ingredient(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    purchased_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=254)
    expired = models.BooleanField(default=False)
    store = models.ForeignKey(Store, on_delete=models.PROTECT)