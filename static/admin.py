from django.contrib import admin
from .models import News
from .models import Tasks

admin.site.register(News)
admin.site.register(Tasks)
