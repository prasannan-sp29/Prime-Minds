from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Sale, Delivery, Medicine
import datetime

def get_order_number(pk):
    ord_num = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    order_number = ord_num + str(pk)
    return order_number 

@receiver(post_save, sender=Sale)
def create_delivery(sender, instance, created, **kwargs):
    if created:
        Delivery.objects.create(sale=instance,order_number=get_order_number(instance.id))
        

@receiver(post_save, sender=Delivery)
def update_stock(sender, instance, **kwargs):
    if instance.status == 'DELIVERED':
        sale = instance.sale
        medicine = sale.medicine
        medicine.stock -= sale.quantity
        medicine.save()
