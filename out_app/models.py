from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils.crypto import get_random_string
from django.utils.text import slugify


STATUS = ((0, "Draft"), (1, "Ready to Send"))


class Page(models.Model):
    """
    Class for modelling posts made by creators.
    """
    slug = models.SlugField("Page code", max_length=12, unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="related_creator", default=User)
    text_content = models.TextField()
    image = CloudinaryField(blank=True)
    link = models.TextField(blank=True)
    link_title = models.CharField(max_length=250, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)


    def __str__(self):
        return self.creator

