from django.contrib import admin

# Register your models here.

from .models import Embedded,UserImage,Crops
admin.site.register(Embedded)
admin.site.register(UserImage)
admin.site.register(Crops)
