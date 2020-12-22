from django.contrib import admin
import mysite.models
from django.apps import apps

# Register your models here.

models = apps.get_models()

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
