from django.contrib import admin

from .models import InputModel, VariableSet, ResultSet

# Register your models here.

admin.site.register(InputModel)
admin.site.register(VariableSet)
admin.site.register(ResultSet)
