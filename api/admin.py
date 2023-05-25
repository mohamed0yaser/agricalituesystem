from django.contrib import admin

# Register your models here.

from .models import Embedded,UserImage,Crops,SelectedCrop
admin.site.register(Embedded)
admin.site.register(UserImage)
admin.site.register(Crops)
admin.site.register(SelectedCrop)
