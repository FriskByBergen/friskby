from django.contrib import admin
from models import *

class ApiKeyAdmin(admin.ModelAdmin):
    readonly_fields = ('external_key',)
    
admin.site.register(ApiKey, ApiKeyAdmin)

