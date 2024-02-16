# emall/user/tests.py
import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger("django")

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('registration')
        data = {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'mobile': '123456789'}
        response = self.client.post(url, data, format='json')

        logger.info(f"USER_TEST |  Registration API Response : {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    # def test_user_login(self):
    #     # Assuming you have implemented the TokenObtainPairView for JWT token
    #     url = reverse('token_obtain_pair')
    #     data = {'username': 'testuser', 'password': 'testpass'}
    #     response = self.client.post(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertIn('access', response.data)
    #     self.assertIn('refresh', response.data)

    # def test_invalid_password_change(self):
    #     # Assuming you have implemented the ChangePasswordView for password change
    #     url = reverse('change-password')
    #     data = {'old_password': 'testpass', 'new_password': 'newpass123'}
    #     response = self.client.put(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('non_field_errors', response.data)

  
