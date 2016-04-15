from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Image
from django.test import Client
import factory
import os
from imagersite.settings import BASE_DIR


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    photo = factory.django.ImageField(color='blue')


class TestProfile(TestCase):

    def setUp(self):
        self.test_user1 = User.objects.create_user('testuser',
                                                   'test@test.com',
                                                   'testpassword')
        self.test_user1.save()
        self.image1 = PhotoFactory.create(title='image 1',
                                          owner=self.test_user1,
                                          published='Public')
        self.image2 = PhotoFactory.create(title='image 2',
                                          owner=self.test_user1)
        self.image1.save()
        self.image2.save()

        self.unauth = Client()

        self.auth = Client()
        self.auth.login(username='testuser', password='testpassword')

    def tearDown(self):
        os.remove(os.path.join(BASE_DIR,
                               'media/{}'.format(self.image1.photo.url)))
        os.remove(os.path.join(BASE_DIR,
                               'media/{}'.format(self.image2.photo.url)))

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

    def test_public_image_in_response(self):
        response = self.unauth.get('/')
        self.assertTrue(self.image1.photo.url in str(response.content))

    def test_private_image_not_in_response(self):
        response = self.unauth.get('/')
        self.assertTrue(self.image2.photo.url not in str(response.content))
