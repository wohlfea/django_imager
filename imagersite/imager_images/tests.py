from django.test import TestCase
from django.contrib.auth.models import User
from .models import Album, Image
from datetime import datetime
from django.test import Client
from django.db.models.fields.files import ImageFieldFile
import factory
import os
from imagersite.settings import BASE_DIR


class PhotoFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Image

    photo = factory.django.ImageField(color='blue')


class TestImages(TestCase):
    """Test Albums and Images and their relationships."""
    def setUp(self):
        self.test_user1 = User.objects.create_user('test user',
                                                   'test@test.com',
                                                   'testpassword')
        self.test_user1.save()
        self.album1 = Album(title='album 1', owner=self.test_user1)
        self.album2 = Album(title='album 2', owner=self.test_user1)
        self.image1 = PhotoFactory.create(title='image 1',
                                          owner=self.test_user1)
        self.image2 = PhotoFactory.create(title='image 2',
                                          owner=self.test_user1)
        self.album1.save()
        self.album2.save()
        self.image1.save()
        self.image2.save()
        self.image1.albums.add(self.album1)

    def tearDown(self):
        os.remove('{}{}'.format(BASE_DIR, self.image1.photo.url))
        os.remove('{}{}'.format(BASE_DIR, self.image2.photo.url))

    def test_album_exists(self):
        """Test album has been created."""
        self.assertIsInstance(self.album1, Album)

    def test_image_exists(self):
        """Test image has been created."""
        self.assertIsInstance(self.image1, Image)

    def test_album_title(self):
        """Test album has title."""
        self.assertEquals(self.album1.title, 'album 1')

    def test_image_title(self):
        """Test image has title."""
        self.assertEquals(self.image1.title, 'image 1')

    def test_album_default_description(self):
        """Test album default description is empty string."""
        self.assertEquals(self.album1.description, '')

    def test_image_default_description(self):
        """Test image default description is empty string."""
        self.assertEquals(self.image1.description, '')

    def test_album_date_uploaded(self):
        """Test to verify date for date uploaded on album."""
        self.assertIsInstance(self.album1.date_uploaded, datetime)

    def test_image_date_uploaded(self):
        """Test to verify date for date uploaded on image."""
        self.assertIsInstance(self.image1.date_uploaded, datetime)

    def test_album_date_modified(self):
        """Test to verify the date changes upon modification."""
        initial = self.image1.date_modified
        self.assertEquals(initial, self.image1.date_modified)
        self.image1.title = 'new title'
        self.image1.save()
        self.assertNotEqual(initial, self.image1.date_modified)

    def test_image_in_album(self):
        """Test to verify that image can be in album."""
        self.assertEquals(self.album1.images.all()[0], self.image1)

    def test_images_have_owner(self):
        """Test to verify that images have owners."""
        self.assertEquals(self.image1.owner, self.test_user1)

    def test_albums_have_owner(self):
        """Test to verify that albums have owners."""
        self.assertEquals(self.album1.owner, self.test_user1)

    def test_user_has_albums(self):
        """Test to verify that user has albums."""
        self.assertEquals(self.test_user1.albums.all().count(), 2)

    def test_user_has_images(self):
        """Test to verify that user has images."""
        self.assertEquals(self.test_user1.images.all().count(), 2)

    def test_image_has_image(self):
        """Test to verify image has been created with an image."""
        self.assertIsInstance(self.image1.photo, ImageFieldFile)


class TestViews(TestCase):

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

    def test_unauth_add_photo_response(self):
        """Test unauthed user can't get to photo add page."""
        response = self.unauth.get('/images/photo/add/')
        self.assertEquals(response.status_code, 302)

    def test_auth_add_photo_response(self):
        """Test authed user can get to photo add page."""
        response = self.auth.get('/images/photo/add/')
        self.assertEquals(response.status_code, 200)

    def test_unauth_add_album_response(self):
        """Test unauthed user can't get to album add page."""
        response = self.unauth.get('/images/album/add/')
        self.assertEquals(response.status_code, 302)

    def test_auth_add_album_response(self):
        """Test authed user can get to photo add page."""
        response = self.auth.get('/images/album/add/')
        self.assertEquals(response.status_code, 200)
