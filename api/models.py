from django.db import models
from django.contrib.auth.models import User



class Embedded(models.Model):
    temperature=models.FloatField(max_length=255)
    humidity=models.FloatField(max_length=255)
    light=models.CharField(max_length=255)
    rainfall=models.FloatField(max_length=255)
    soil_moisture=models.FloatField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    pump_on = models.BooleanField(default=False)



    def __str__(self):
        
        return f"{self.temperature} {self.humidity} {self.light} {self.rainfall} {self.soil_moisture}{self.pump_on}"
    class Meta:
        ordering = ['-updated']


# lets us explicitly set upload path and filename
def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

class UserImage(models.Model):
    
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    creation_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-creation_date']

class Crops(models.Model):
    crop_name = models.CharField(max_length=255)
    soil_moisture_min=models.FloatField(max_length=255)
    soil_moisture_max=models.FloatField(max_length=255)
    
    def __str__(self):
        return f"{self.crop_name}{self.soil_moisture_min}{self.soil_moisture_max}"

class SelectedCrop(models.Model):
    crop = models.OneToOneField(Crops, on_delete=models.CASCADE)
    soil_moisture_min=models.FloatField(max_length=255)
    soil_moisture_max=models.FloatField(max_length=255)
    
    def __str__(self):
        return f"{self.crop}{self.soil_moisture_min}{self.soil_moisture_max}"


class ReportPlant(models.Model):
    plant_name = models.CharField(max_length=255)
    confidence = models.FloatField(max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.plant_name}"






