
# Test cases in Python.

Pytest: An Introduction

What is Pytest?: Pytest is a testing framework for Python that simplifies the process of writing and executing test cases for your Python code.

Purpose: Pytest is designed to make testing easy and scalable. It provides a simple syntax for writing tests, powerful features for test discovery and execution, and support for various types of tests.

Installation: You can install Pytest using pip. Open your terminal or command prompt and run the following command:

* pip install pytest

Setup: After installation, you can create test files using the naming convention test_*.py or *_test.py. Pytest will automatically discover and run these files.

* Advantages:

Simple Syntax: Pytest uses a simple and concise syntax for writing tests, making it easy to learn and use.
Powerful Features: Pytest offers powerful features such as fixtures, parameterized testing, and built-in support for assertions.
Test Discovery: Pytest automatically discovers and runs tests, eliminating the need for explicit test suite setup.
* Limitations:
 While Pytest is a versatile testing framework, it may have a learning curve for beginners. Additionally, some specific testing scenarios might require additional plugins or configurations.

# Example Pytest Test:

Create a file named test_user.py

# test_user.py

from app.user.user_models import User

def test_create_user():
    # Your test logic for creating a user
    assert User.objects.create(username='testuser', password='testpass')

def test_user_properties():
    user = User(username='testuser', password='testpass')
    assert user.username == 'testuser'
    assert user.check_password('testpass')

# test_order.py

from app.orders.models import Orders

# test_order.py

from app.orders.models import Orders

def test_create_order():
    # Your test logic for creating an order
    order = Orders.objects.create(order_id='123', amount=50.0, customer='testcustomer', order_status='PENDING')
    assert order is not None
    assert order.order_id == '123'
    assert order.amount == 50.0
    assert order.customer == 'testcustomer'
    assert order.order_status == 'PENDING'

# Run pytest

* pytest

Types of Assertions:

Equality Assertion (assert a == b): Compares if two values are equal.
Inequality Assertion (assert a != b): Compares if two values are not equal.
Identity Assertion (assert a is b): Checks if two objects refer to the same instance.
Inequality Identity Assertion (assert a is not b): Checks if two objects do not refer to the same instance.
Truthiness Assertion (assert a or assert not a): Checks if a value is considered True or False.


# Django Test Cases (Unit Testing)

What is Unit Testing in Django?
Unit testing is a software testing method where individual units or components of a software application are tested in isolation to ensure they work as expected. In the context of Django, unit testing involves testing individual functions, methods, or classes within your Django application.

Advantages of Unit Testing in Django:
Early Bug Detection:

Helps catch bugs and errors early in the development process.
Isolation of Issues:

Allows you to identify and fix issues in specific parts of your code without affecting the entire application.
Documentation:

Serves as a form of documentation, showing how each part of your code is expected to behave.
Refactoring Support:

Provides confidence that existing functionality still works after code refactoring.
Continuous Integration:

Facilitates integration with continuous integration (CI) systems for automated testing.
Use Cases for Django Unit Testing:
Models:

Test database models and their methods.
Views:

Test the behavior of Django views, especially the logic handling requests.
Forms:

Validate form behavior and data processing.
Utility Functions:

Ensure that utility functions and helper methods produce the correct output.
Difference from Pytest:
Django Unit Testing is part of the Django framework and comes with its own set of testing tools. It uses the unittest module, which is inspired by the Java testing framework JUnit. Django's testing tools are integrated into the framework and provide features specific to Django applications.

Pytest, on the other hand, is a third-party testing framework widely used in the Python ecosystem. It is not Django-specific but can be used for testing Django applications. Pytest provides a simpler syntax, powerful fixtures, and a rich set of plugins, making it popular among Python developers.

How to Use Django Unit Testing:
Write Test Classes:

Create test classes that inherit from django.test.TestCase.
Define Test Methods:

Write methods within your test class to test specific functionalities.
Assertions:

Use various assertions provided by the unittest module to verify expected outcomes.
Run Tests:

Use Django management commands to run your tests, such as python manage.py test.
Assertion Tests:
Assertions are statements that assert or confirm a condition. In Django unit testing, common assertions include:

self.assertEqual(a, b): Check if a is equal to b.
self.assertTrue(expr): Check if expr evaluates to True.
self.assertFalse(expr): Check if expr evaluates to False.

# Example Django Test Class:
from django.test import TestCase
from myapp.models import MyModel

class MyModelTestCase(TestCase):
    def setUp(self):
        MyModel.objects.create(name="Test Model")

    def test_model_name(self):
        model_instance = MyModel.objects.get(name="Test Model")
        self.assertEqual(model_instance.name, "Test Model")

* Use the following command to run tests:
 # python manage.py test
