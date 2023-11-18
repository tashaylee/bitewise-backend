from django.contrib import admin
from store.models import Store


class StoreAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


admin.site.register(Store, StoreAdmin)
