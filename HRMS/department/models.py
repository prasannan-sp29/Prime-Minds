from django.db import models

# Create your models here.

class dept(models.Model):
    d_name = models.CharField(max_length=100)

    def __str__(self):
        return self.d_name
