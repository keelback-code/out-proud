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
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="allowed_page")
    text_content = models.TextField()
    image = CloudinaryField(blank=True)
    link = models.TextField(blank=True)
    link_title = models.CharField(max_length=250, blank=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.title


class ViewerAccess(models.Model):
    """
    Class for assigning pages to viewers
    """
    allowed_page = models.ForeignKey(Page, on_delete=models.CASCADE, verbose_name="Page code - this can be found on your profile page")
    shown_name = models.CharField("Your name (as it will appear to viewer)", max_length=100)
    first_name = models.CharField("The name of the viewer you are sending this to", max_length=100)
    email = models.EmailField(max_length=100, primary_key=True)


    def __str__(self):
        return str(self.first_name)

