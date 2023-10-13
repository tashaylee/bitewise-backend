from django.contrib import admin
from commitment.models import *


class CommitmentCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'year', 'month', 'week', 'count', 'created_at')

class MealCommitmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'cost', 'achieved', 'activated', 'commitment_count')



admin.site.register(CommitmentCount, CommitmentCountAdmin)
admin.site.register(MealCommitment, MealCommitmentAdmin)