from django.db import models
from django.contrib.auth.models import User
from department.models import dept

# Create your models here.
class userdetials(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    password_token = models.CharField(max_length=100)

    # department_name = models.ForeignKey(dept,on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.user.username}"