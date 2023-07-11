from django.core.exceptions import BadRequest


class DataMixin:
    def __init__(self):
        self.data = None

    def is_get_field_from_data(self, filed_name, **kwargs):
        self.data = kwargs.get('data')
        if not self.data.get(filed_name):
            raise BadRequest
        return self.data.get('data').get(filed_name)
