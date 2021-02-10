from django.db import models


# Create your models here.
class BSE(models.Model):
    CODE = models.CharField(max_length=20)
    NAME = models.CharField(max_length=20)
    OPEN = models.FloatField()
    HIGH = models.FloatField()
    LOW = models.FloatField()
    CLOSE = models.FloatField()

    def __str__(self):
        return self.NAME
