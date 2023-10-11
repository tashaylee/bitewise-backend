from django.db.models.signals import post_save
from django.dispatch import receiver
from .commitment.models import *


@receiver(post_save, sender=CommitmentCount)
def associate_meal_commitment(sender, instance, created,  **kwargs):
    count = instance.count
    for i in range(count):
        MealCommitment.objects.create(commitment_count=instance)
    return