from rest_framework.test import APITestCase
from rest_framework import status
from .models import ExtendedUser
from accounts.models import Account


class UserTestCase(APITestCase):
  def setUp(self):
    account = Account.objects.create(account_name='SafetyVision')
    user_data = {
      'first_name': 'Safety',
      'last_name': 'Supervisor',
      'email': 'safetysupervisor@safetyvision.ca',
      'password': 'supersafesupervisorpassword123',
    }
    user = ExtendedUser.objects.create(
      first_name=user_data['first_name'],
      last_name=user_data['last_name'],
      account=account,
      email=user_data['email'],
      username=user_data['email'],
    )
    user.set_password(user_data['password'])
    user.save()
    self.client.login(
      username=user_data['email'],
      password=user_data['password'],
    )

  def tearDown(self):
    self.client.logout()

  def test_create_a_new_user(self):
    current_users_count = ExtendedUser.objects.count()
    url = '/api/users/'
    user = {
      'first_name': 'Bob',
      'last_name': 'Obo',
      'email': 'bobobo@obobob.com',
      'password': 'supersecretpassword123',
    }

    response = self.client.post(url, user, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertEqual(ExtendedUser.objects.count(), current_users_count + 1)
    self.assertEqual(response.data['first_name'], user['first_name'])
    self.assertEqual(response.data['last_name'], user['last_name'])
    self.assertEqual(response.data['email'], user['email'])
