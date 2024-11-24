from django.db import models

class CloudinaryImage:

    def __init__(self, public_id, url, created_at, description=''):
        self.public_id = public_id
        self.url = url
        self.created_at = created_at
        self.description = description

    def __str__(self):
        return self.public_id
