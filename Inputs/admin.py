from django.contrib import admin

from .models import InputModel, VariableSet, LookupSet

# Register your models here.

admin.site.register(InputModel)
admin.site.register(VariableSet)
admin.site.register(LookupSet)