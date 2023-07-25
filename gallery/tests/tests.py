# import json
#
# from django.test import TransactionTestCase
# from http import HTTPStatus as HttpStatusCode
#
# from gallery.models import Image
#
#
# # Create your tests here.
#
#
# class ImageModelViewPostMethodTestCase(TransactionTestCase):
#    """
#    Image collection test case implementation.
#    """
#
#     reset_sequences = True
#
#     def setUp(self):
#         """
#         Set up data for tests.
#         """
#         self.test_image_1 = Image.objects.create(
#             title='test_image_1',
#             gallery='...'
#         )
#         self.test_image_2 = Image.objects.create(
#             title='test_image_2',
#             gallery='...'
#         )
#
#     def test_images(self):
#         test_images = Image.objects.all()
#
#         assert test_images[0] == self.test_image_1
#         assert test_images[1] == self.test_image_2
