from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class userdetials(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    DOB = models.DateField()
    date_of_join = models.DateField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_number = models.BigIntegerField()
    alternate_phone_number = models.BigIntegerField(blank=True)
    bank_name = models.CharField(max_length=50)
    bank_acc_number = models.BigIntegerField()
    mail_id = models.EmailField()
    aadhar_no = models.BigIntegerField()
    pan_number = models.CharField(max_length=20)
    # department = models.ForeignKey(dept, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile', blank=True)
    # salary = models.BigIntegerField()

    # def __str__(self):
    #     return self.user

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField(blank=True)
    phone_number = models.BigIntegerField(blank=True)
    alternate_phone_number = models.BigIntegerField(blank=True)
    mail_id = models.EmailField()
    role = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile', blank=True)
