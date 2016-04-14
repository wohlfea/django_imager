from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client


class TestProfile(TestCase):
    def setUp(self):
        self.test_user1 = User.objects.create_user('testuser',
                                                   'test@test.com',
                                                   'password')
        self.test_user1.save()

        self.unauth = Client()
        # self.auth = Client()
        #
        # self.auth.post(
        #     '/account/login/',
        #     {'username': 'testuser', 'password': 'password'}
        #     )

    def test_unauth_home_response(self):
        response = self.unauth.get('/')
        self.assertEquals(response.status_code, 200)

    def test_unauth_login_response(self):
        response = self.unauth.get('/accounts/login')
        self.assertEquals(response.status_code, 301)

    def test_unauth_register_response(self):
        response = self.unauth.get('/accounts/register/')
        self.assertEquals(response.status_code, 200)

    def test_auth_home_response(self):
        response = self.unauth.get('/')
        self.assertEquals(response.status_code, 200)

    def test_unauth_login(self):
        self.unauth.get('/accounts/login')
        response = self.unauth.post(
            '/account/login/',
            {'username': 'testuser', 'password': 'password'},
            follow=True
            )
        self.assertEquals(response.status_code, 301)
