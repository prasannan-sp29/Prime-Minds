from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    role = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    emp_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.BigIntegerField()
    salary = models.BigIntegerField()
    mail_id = models.EmailField()
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=20,null=True, blank=True)
    address = models.CharField(max_length=100,null=True, blank=True)
    city = models.CharField(max_length=100,null=True, blank=True)
    state = models.CharField(max_length=100,null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    phone_number = models.BigIntegerField(null=True, blank=True)
    # alternate_phone_number = models.BigIntegerField(null=True, blank=True)
    mail_id = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=20,null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=100)
    tablet_name = models.CharField(max_length=100)
    price = models.IntegerField()
    # comapny_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    mail_id = models.EmailField()
    # Gender = models.CharField(max_length=100)   

    def __str__(self):
        return self.dealer_name

class Medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    medicine_code = models.CharField(max_length=20)
    dealer_name = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    price = models.IntegerField()
    stock = models.PositiveIntegerField()
    company_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    # mfg_date = models.DateField()
    # exp_date = models.DateField()

    def __str__(self):
        return self.medicine_name




# class Customer(models.Model):
#     name = models.CharField(max_length=100)
#     phone_number = models.CharField(max_length=15)

#     def __str__(self):
#         return self.name


class Purchase(models.Model):
    tablet_name = models.ForeignKey(Medicine,on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    # dealer_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_amount = self.price * self.quantity
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.tablet_name} from {self.customer}"


class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    medicine = models.ForeignKey(Medicine,on_delete=models.CASCADE,blank=True)
    # tablet_name = models.CharField(max_length=100)
    phone = models.BigIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    confirmed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        subtotal = self.price * self.quantity
        discount_amount = subtotal * (self.discount / 100)
        total_after_discount = subtotal - discount_amount
        tax_amount = total_after_discount * (self.tax / 100)
        self.total = total_after_discount + tax_amount
        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.first_name} - {self.tablet_name}"


class Delivery(models.Model):
    order_number = models.CharField(max_length=20)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    status = models.CharField(max_length=30, default='PENDING')

    def __str__(self):
        return f"Delivery for Sale: {self.sale}"

