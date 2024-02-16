# emall/user/tests.py
import logging
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient,APITestCase
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken

User = get_user_model()
logger = logging.getLogger("django")

class UserAuthenticationTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_user_registration(self):
        url = reverse('registration')
        data = {'username': 'testuser', 'password': 'testpass', 'email': 'test@example.com', 'mobile': '123456789'}
        response = self.client.post(url, data, format='json')
        # logger.info(f"USER_TEST |  Registration API Response : {response.data}")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    # def test_user_login(self):
    #     # Assuming you have implemented the TokenObtainPairView for JWT token
    #     url = reverse('token_obtain_pair')
    #     data = {'username': 'testuser', 'password': 'testpass'}
    #     response = self.client.post(url, data, format='json')

    #     logger.info(f"USER_TEST |  Login API Response : {response.data}")
        # self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertIn('access', response.data)
        # self.assertIn('refresh', response.data)

    # def test_invalid_password_change(self):
    #     # Assuming you have implemented the ChangePasswordView for password change
    #     url = reverse('change-password')
    #     data = {'old_password': 'testpass', 'new_password': 'newpass123'}
    #     response = self.client.put(url, data, format='json')

    #     self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    #     self.assertIn('non_field_errors', response.data)

  


class UserLoginAPITest(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='demo', email='demo@example.com', 
                                            mobile='1234567890', password='TestPassword123')
        self.login_url = reverse('token_obtain_pair')  # Replace 'login' with the actual URL name for login

    def test_user_login_response(self):
        data = {
            "username": "demo",
            "password": "TestPassword123",
        }

        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response.data)
        # self.assertTrue('token' in response.data)




# Admin API Test cases
class ViewUsersAPITestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username='test_user', password='password', email="test_user@example.com",
             user_scope='ADMIN', mobile='2345698710',
        )
        self.base_url = "/api/v1"
        self.token = AccessToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        self.user_1 = User.objects.create(
            username='demo_user_1', first_name='Demo', last_name='User 1', email='demo1@example.com',
             user_scope='USER', mobile='1234567890',
        )
        self.user_2 = User.objects.create(
            username='demo_user_2', first_name='Demo', last_name='User 2', email='demo2@example.com',
            user_scope='USER', mobile='9876543210'
        )


    
    def test_list_users(self):
        response = self.client.get(f'{self.base_url}/users/')
        print(response.data)
        self.assertEqual(response.status_code, 200)
       




# Swagger Documentation