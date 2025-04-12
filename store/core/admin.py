from django.contrib import admin

from .models import Bussiness

class BussinessAdmin(admin.ModelAdmin):
    list_display = ('matricule_fiscale', 'name', 'address', 'city', 'country', 'phone', 'email', 'created_at', 'type')
    search_fields = ('matricule_fiscale', 'name', 'address', 'city', 'country', 'phone', 'email')
    list_filter = ('created_at', 'type')

admin.site.register(Bussiness)

