from django.db import models

class banners(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='banners/')

    def __str__(self):
        return self.title