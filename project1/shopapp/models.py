from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # username = models.CharField(max_length=20)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    # DOB = models.DateField()
    # date_of_join = models.DateField()
    # address = models.CharField(max_length=100)
    # city = models.CharField(max_length=100)
    # state = models.CharField(max_length=100)
    # pincode = models.IntegerField()
    phone_number = models.BigIntegerField()
    # alternate_phone_number = models.BigIntegerField(null=True, blank=True)
    # bank_name = models.CharField(max_length=50)
    # bank_acc_number = models.BigIntegerField()
    mail_id = models.EmailField()
    # aadhar_no = models.BigIntegerField()
    # pan_number = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField(max_length=50)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    password = models.CharField(max_length=20)
    pincode = models.IntegerField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    alternate_phone_number = models.BigIntegerField(null=True, blank=True)
    mail_id = models.EmailField()
    role = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    price = models.IntegerField()
    dosageform = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100)
    mfg_date = models.DateField()
    exp_date = models.DateField()

    def __str__(self):
        return self.medicine_name

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=100)
    tablet_name = models.CharField(max_length=100)
    price = models.IntegerField()
    comapny_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    Gender = models.CharField(max_length=100)
    Date = models.DateField(auto_created=10)    

    def __str__(self):
        return self.dealer_name