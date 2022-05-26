import random
import string
from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


def random_str_generator(chars=string.ascii_lowercase + string.digits):
    """
    Function for creating random slugs.
    """
    return ''.join(random.choice(chars) for _ in range(6))


class Page(models.Model):
    """
    Class for modelling pages made by creators.
    """
    slug = models.SlugField(unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="allowed_page")
    text_content = models.TextField()
    image = CloudinaryField(blank=True, default="placeholder")
    link = models.CharField(
        max_length=500,
        verbose_name="Link - see Resources page for options",
        blank=True)
    link_title = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.title

    # def slug_gen(self):
    #     slug = random_str_generator()
    #     return self.slug

    def save(self, *args, **kwargs):  # add docstring for this later
        # if self.slug:
        self.slug = random_str_generator()
        super().save(*args, **kwargs)


class ViewerAccess(models.Model):
    """
    Class for assigning pages to viewers.
    """
    allowed_page = models.ForeignKey(
        Page,
        on_delete=models.CASCADE,
        verbose_name="Page you would like the recipient to see")
    shown_name = models.CharField(
        "Your name (as it will appear to viewer)",
        max_length=100)
    first_name = models.CharField(
        "The name of the viewer you are sending this to",
        max_length=100)
    viewer_email = models.EmailField(
        max_length=100,
        unique=True,
        primary_key=True)

    def __str__(self):
        return self.viewer_email

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
