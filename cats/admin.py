from django.contrib import admin

from .models import Cat, Owner


admin.site.register(Cat)
admin.site.register(Owner)