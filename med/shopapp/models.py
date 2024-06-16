# models.py
from django.db import models
from django.contrib.auth.models import User
from .validators import validate_phone_number
import datetime

class UserDetails(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, verbose_name="User Role")

    def __str__(self):
        return self.user.username

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    emp_id = models.CharField(max_length=10)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=10)
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
    password = models.CharField(max_length=20, null=True, blank=True)
    address = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    phone_number = models.CharField(
        max_length=10,
        validators=[validate_phone_number],
        null=True,
        blank=True
    )
    mail_id = models.EmailField(null=True, blank=True)
    role = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Dealer(models.Model):
    dealer_name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    mail_id = models.EmailField()

    def __str__(self):
        return self.dealer_name

class Tablet(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE, null=True, blank=True)
    tablet_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.tablet_name

class Contact(models.Model):
    name = models.CharField(max_length=20)
    phone = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )

    def __str__(self):
        return self.name

class Medicine(models.Model):
    medicine_name = models.ForeignKey(Tablet, on_delete=models.CASCADE)
    medicine_code = models.CharField(max_length=20)
    dealer_name = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    company_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)

    def __str__(self):
        return str(self.medicine_name)

class Purchase(models.Model):
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0.00)

    def calculate_total_amount(self):
        total = sum(item.price * item.quantity for item in self.purchaseitem_set.all())
        return total

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Purchase, self).save(*args, **kwargs)
        self.total_amount = self.calculate_total_amount()
        super(Purchase, self).save(*args, **kwargs)

    def __str__(self):
        return f"Purchase from {self.dealer}"

class PurchaseItem(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    tablet_name = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        super(PurchaseItem, self).save(*args, **kwargs)
        self.purchase.save()

def get_order_number():
    ord_num = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number = ord_num
    return order_number

SALE_STATUS_CHOICES = [
    ('SALE COUNTER', 'SALE COUNTER'),
    ('SALE DELIVERY', 'SALE DELIVERY'),
]

class Sale(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    phone = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=5, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)
    confirmed = models.CharField(max_length=20, choices=SALE_STATUS_CHOICES, default='SALE ORDER')

    def save(self, *args, **kwargs):
        if self.pk:
            subtotal = sum(item.total for item in self.items.all())
            discount_amount = subtotal * (self.discount / 100)
            total_after_discount = subtotal - discount_amount
            tax_amount = total_after_discount * (self.tax / 100)
            self.total = total_after_discount + tax_amount

            # Check if sale is confirmed and create delivery if it is
            if self.confirmed in ['SALE DELIVERY'] and not Delivery.objects.filter(sale=self).exists():
                delivery = Delivery.objects.create(
                    sale=self,
                    order_number=get_order_number() + str(self.pk),
                    status='PENDING'
                )
                # Add sale items to delivery
                for item in self.items.all():
                    delivery.sale_items.add(item)

        super(Sale, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.customer.first_name} - {self.id}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super(SaleItem, self).save(*args, **kwargs)
        self.sale.save()

    def __str__(self):
        return f"{self.medicine.medicine_name} (x{self.quantity})"

class Delivery(models.Model):
    order_number = models.CharField(max_length=20)
    sale = models.OneToOneField(Sale, on_delete=models.CASCADE)
    sale_items = models.ManyToManyField(SaleItem)
    status = models.CharField(max_length=30, default='PENDING')

    def __str__(self):
        return f"Delivery for Sale: {self.sale}"

class Lead(models.Model):
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    tablet_name = models.CharField(max_length=100)
    email = models.EmailField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

class Opportunity(models.Model):
    lead = models.ForeignKey(Lead, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    tablet_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name

class SalesOrder(models.Model):
    opportunity = models.ForeignKey(Opportunity, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=100)
    phone_number = models.CharField(
        max_length=10,
        validators=[validate_phone_number]
    )
    tablet_name = models.CharField(max_length=100)
    price = models.FloatField()
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.customer_name
