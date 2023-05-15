from django.db import models



class Embedded(models.Model):
    temperature=models.FloatField(max_length=255)
    humidity=models.FloatField(max_length=255)
    light=models.FloatField(max_length=255)
    rainfall=models.FloatField(max_length=255)
    soil_moisture=models.FloatField(max_length=255)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    pump_on = models.BooleanField(default=False)



    def __str__(self):
        
        return f"{self.temperature} {self.humidity} {self.light} {self.rainfall} {self.soil_moisture}{self.pump_on}"
    class Meta:
        ordering = ['-updated']


class UserImage(models.Model):
    name = models.CharField(null=True, blank=True, max_length=50)
    user_Img = models.ImageField(null=True, blank=True, upload_to='images/')


class Crops(models.Model):
    crop = models.CharField(max_length=255)
    soil_moisture_min=models.FloatField(max_length=255)
    soil_moisture_max=models.FloatField(max_length=255)
    
    def __str__(self):
        return f"{self.crop}{self.soil_moisture_min}{self.soil_moisture_max}"







