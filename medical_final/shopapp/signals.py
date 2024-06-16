from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
import datetime

def get_order_number(pk):
    ord_num = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number = ord_num + str(pk)
    return order_number 

@receiver(post_save, sender=Sale)
def create_delivery(sender, instance, created, **kwargs):
    if instance.confirmed =='SALE DELIVERY' and not Delivery.objects.filter(sale=instance).exists():
        Delivery.objects.create(sale=instance, order_number=get_order_number(instance.id))

@receiver(post_save, sender=Delivery)
def update_stock(sender, instance, **kwargs):
    if instance.status == 'DELIVERED':
        for item in instance.sale.items.all():
            tablet = item.medicine
            tablet.stock -= item.quantity
            tablet.save()

@receiver(post_save, sender=Lead)
def create_opportunity(sender, instance, **kwargs):
    if instance.status:  
        Opportunity.objects.create(
            lead=instance,
            customer_name=instance.name,
            phone_number=instance.phone,
            tablet_name=instance.tablet,
            price=instance.price,
            quantity=instance.quantity
        )

@receiver(post_save, sender=Opportunity)
def create_saleorder(sender, instance, **kwargs):
    if instance.status:  
        SalesOrder.objects.create(
            opportunity=instance,
            customer_name=instance.customer_name,
            phone_number=instance.phone_number,
            tablet_name=instance.tablet_name,
            price=instance.price,
            quantity=instance.quantity
        )
