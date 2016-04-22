from django.test import TestCase
from django.contrib.auth.models import User
from imager_images.models import Album, Image
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
        """Setup users, images, albums, auth & unauth clients."""
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
        self.album1 = Album(title='My Album', owner=self.test_user1,
                            cover=self.image1.photo)
        self.album1.save()

        self.unauth = Client()

        self.auth = Client()
        self.auth.login(username='testuser', password='testpassword')

    def tearDown(self):
        """Delete temporary pictures."""
        os.remove('{}{}'.format(BASE_DIR, self.image1.photo.url))
        os.remove('{}{}'.format(BASE_DIR, self.image2.photo.url))

    def test_unauth_home_response(self):
        """Test anyone can get to home page."""
        response = self.unauth.get('/')
        self.assertEquals(response.status_code, 200)

    def test_unauth_login_response(self):
        response = self.unauth.get('/accounts/login')
        self.assertEquals(response.status_code, 301)

    def test_unauth_register_response(self):
        """Test anyone can get to register page."""
        response = self.unauth.get('/accounts/register/')
        self.assertEquals(response.status_code, 200)

    def test_public_image_in_response(self):
        """Verify public image shows up on homepage."""
        response = self.unauth.get('/')
        self.assertTrue(self.image1.photo.url in str(response.content))

    def test_private_image_not_in_response(self):
        """Verify private image does not show up on home page."""
        response = self.unauth.get('/')
        self.assertTrue(self.image2.photo.url not in str(response.content))

    def test_profile_logged_out(self):
        """Redirect upon attempting to get to profile page if logged out."""
        response = self.unauth.get('/accounts/profile')
        self.assertTrue(response.status_code == 302)

    def test_profile_logged_in(self):
        """Access to profile page if logged in."""
        response = self.auth.get('/accounts/profile')
        self.assertEquals(response.status_code, 200)

    def test_profile_image_count(self):
        """Photo count shown on profile page."""
        response = self.auth.get('/accounts/profile')
        self.assertTrue('Total Photos: 2' in str(response.content))

    def test_profile_album_count(self):
        """Album count shown on profile page."""
        response = self.auth.get('/accounts/profile')
        self.assertTrue('Total Albums: 1' in str(response.content))

    def test_library_logged_out(self):
        """Redirect if unauthorized on library page."""
        response = self.unauth.get('/images/library')
        self.assertEquals(response.status_code, 302)

    def test_library_logged_in(self):
        """Access to library page if logged in."""
        response = self.auth.get('/images/library')
        self.assertEquals(response.status_code, 200)

    def test_library_album_display(self):
        """Verify album titles display in library."""
        response = self.auth.get('/images/library')
        self.assertTrue('My Album' in str(response.content))

    def test_library_image_display(self):
        """Image titles display in image library."""
        response = self.auth.get('/images/library')
        self.assertTrue('image 1' in str(response.content))

    def test_auth_public_image_view(self):
        """Access granted if logged in as user to view private picture."""
        user_id = self.test_user1.id
        image_id = self.image2.id
        response = self.auth.get('/images/image/{}/{}'.format(user_id,
                                                              image_id))
        self.assertEquals(response.status_code, 200)

    def test_unauth_public_image_view(self):
        """Access denied if not authorized to view private picture."""
        user_id = self.test_user1.id
        image_id = self.image2.id
        response = self.unauth.get('/images/image/{}/{}'.format(user_id,
                                                                image_id))
        self.assertEquals(response.status_code, 401)
