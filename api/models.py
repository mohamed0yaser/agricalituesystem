from django.db import models



class Embedded(models.Model):
    temperature=models.FloatField(max_length=255)
    humidity=models.FloatField(max_length=255)
    light=models.FloatField(max_length=255)
    rainfall=models.FloatField(max_length=255)
    soil_moisture=models.FloatField(max_length=255)



    def __str__(self):
        
        return f"{self.temperature} {self.humidity} {self.light} {self.rainfall} {self.soil_moisture}"


class UserImage(models.Model):
    name = models.CharField(max_length=50)
    user_Img = models.ImageField(null=True, blank=True, upload_to='images/')