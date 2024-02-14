#emall/orders/models.py
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.dispatch import receiver
import random
from django.db.models.signals import pre_save, post_save


User = get_user_model()



class OrderStatus():
    ORDER_STATUS = [("PENDING", "Pending"), ("IN_PROGRESS", "IN Progress"),
                   ("SHIPPING", "Shipping"), ("DONE", "Completed"), ]



class Orders(models.Model):
    order_id = models.CharField(max_length=255,null=True,blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, related_name='product_orders')
    customer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='orders')
    address = models.TextField(blank=True)
    remarks = models.TextField(blank=True)
    order_status = models.CharField(max_length=255, choices=OrderStatus.ORDER_STATUS,default="PENDING")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    status = models.BooleanField(default=True) 
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_orders')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='updated_orders')

    def __str__(self):
        return str(self.uuid)

# Generate  Default Order ID 
@receiver(post_save, sender=Orders)
def order_id_gen(sender, instance, created, **kwargs):
    try:
        if not instance.order_id:
            instance.order_id = random.randint(100001, 999999)
            instance.save()
    
    except Exception as ex:
       print(ex)
       pass