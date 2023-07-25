from django.core.files import File
from django.test import TransactionTestCase

from gallery.models import Image


# Create your tests here.


class ImageModelViewPostMethodTestCase(TransactionTestCase):
    """
   Category collection view get method test case implementation.
   """

    reset_sequences = True

    def setUp(self):
        """
        Set up data for tests.
        """
        self.test_image_1 = Image.objects.create(
            name='test_image_1',
            image=File(open('gallery/tests/test_images/test_image1.png', 'rb'))
        )
        self.test_image_2 = Image.objects.create(
            name='test_image_2',
            image=File(open('gallery/tests/test_images/test_image2.png', 'rb'))
        )

    def test_images(self):
        test_images = Image.objects.all()

        assert test_images[0] == self.test_image_1
        assert test_images[1] == self.test_image_2
