from django.contrib import admin

# Register your models here.

from .models import Embedded,UserImage
admin.site.register(Embedded)
admin.site.register(UserImage)
