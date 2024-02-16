
# test_user.py
import os
import sys
# from django.conf import settings
# from orders.models import Orders

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "emall.settings")
# settings.configure()

# def test_create_order():
#     # Your test logic for creating an order
#     order = Orders.objects.create(order_id='123', amount=50.0, customer='testcustomer', order_status='PENDING')
#     assert order is not None
#     assert order.order_id == '123'
#     assert order.amount == 50.0
#     assert order.customer == 'testcustomer'
#     assert order.order_status == 'PENDING'


def add_one(x):
    return x + 1


def test_answer_wrong():
    assert add_one(3) == 5

def test_answer_ok():
    assert add_one(4) == 5