from django.db import models

class FoodProduct(models.Model):
    id = models.IntegerField(primary_key=True)
    category_id = models.IntegerField()
    name = models.TextField()
    name_subtitle = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    pantry_min = models.IntegerField(blank=True, null=True)
    pantry_max = models.IntegerField(blank=True, null=True)
    pantry_metric = models.TextField(blank=True, null=True)
    pantry_tips = models.TextField(blank=True, null=True)
    dop_pantry_min = models.IntegerField(blank=True, null=True)
    dop_pantry_max = models.IntegerField(blank=True, null=True)
    dop_pantry_metric = models.TextField(blank=True, null=True)
    dop_pantry_tips = models.TextField(blank=True, null=True)
    pantry_after_opening_min = models.IntegerField(blank=True, null=True)
    pantry_after_opening_max = models.IntegerField(blank=True, null=True)
    pantry_after_opening_metric = models.TextField(blank=True, null=True)
    refrigerate_min = models.IntegerField(blank=True, null=True)
    refrigerate_max = models.IntegerField(blank=True, null=True)
    refrigerate_metric = models.TextField(blank=True, null=True)
    refrigerate_tips = models.TextField(blank=True, null=True)
    dop_refrigerate_min = models.IntegerField(blank=True, null=True)
    dop_refrigerate_max = models.IntegerField(blank=True, null=True)
    dop_refrigerate_metric = models.TextField(blank=True, null=True)
    dop_refrigerate_tips = models.TextField(blank=True, null=True)
    refrigerate_after_opening_min = models.IntegerField(blank=True, null=True)
    refrigerate_after_opening_max = models.IntegerField(blank=True, null=True)
    refrigerate_after_opening_metric = models.TextField(blank=True, null=True)
    refrigerate_after_thawing_min = models.TextField(blank=True, null=True)
    refrigerate_after_thawing_max = models.TextField(blank=True, null=True)
    refrigerate_after_thawing_metric = models.TextField(blank=True, null=True)
    freeze_min = models.IntegerField(blank=True, null=True)
    freeze_max = models.IntegerField(blank=True, null=True)
    freeze_metric = models.TextField(blank=True, null=True)
    freeze_tips = models.TextField(blank=True, null=True)
    dop_freeze_min = models.IntegerField(blank=True, null=True)
    dop_freeze_max = models.IntegerField(blank=True, null=True)
    dop_freeze_metric = models.TextField(blank=True, null=True)
    dop_freeze_tips = models.TextField(blank=True, null=True)