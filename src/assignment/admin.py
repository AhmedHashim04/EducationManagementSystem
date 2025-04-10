from django.contrib import admin

# Register your models here.
from .models import Assignment , Solution , Grade

admin.site.register(Assignment)

admin.site.register(Solution)

admin.site.register(Grade)