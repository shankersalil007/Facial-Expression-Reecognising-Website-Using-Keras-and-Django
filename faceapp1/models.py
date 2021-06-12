from django.db import models

# Create your models here.

class photo_model(models.Model):
    photo = models.ImageField(upload_to='Images')


class person(models.Model):
    name = models.CharField(max_length=50)
    aadhar_number = models.IntegerField()

    def __str__(self):

        return str(self.id) + "   " +str(self.name)