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
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # date_of_join = models.DateField()
    address = models.CharField(max_length=100,blank=True)  
    state = models.CharField(max_length=100)
    pincode = models.IntegerField()
    phone_number = models.BigIntegerField()
    mail_id = models.EmailField() 
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pincode = models.IntegerField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    # alternate_phone_number = models.BigIntegerField(null=True, blank=True)
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

    def __str__(self):
        return self.dealer_name

from django.db import models

# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    tablet_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        subtotal = self.price * self.quantity
        discount_amount = subtotal * (self.discount / 100)
        total_after_discount = subtotal - discount_amount
        tax_amount = total_after_discount * (self.tax / 100)
        self.total = total_after_discount + tax_amount
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.name} - {self.tablet_name}"

class Purchase(models.Model):
    tablet_name = models.CharField(max_length=100)
    dealer_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tablet_name} from {self.dealer_name}"