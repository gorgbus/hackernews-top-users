from django.contrib import admin
from .models import Comment, StopLoop

# Register your models here.
admin.site.register(Comment)
admin.site.register(StopLoop)