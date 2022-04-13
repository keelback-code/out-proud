from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField


STATUS = ((0, "Draft"), (1, "Ready to Send"))


class Page(models.Model):
    """
    Class for modelling posts made by creators.
    """
    slug = models.SlugField(max_length=8, unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="viewer_creator")
    text_content = models.TextField()
    photo_content = CloudinaryField(blank=True, default='placeholder')
    video_content = CloudinaryField(blank=True)  # large, do I need both of these?
    link = models.TextField(blank=True)
    link_title = models.CharField(max_length=250, blank=True)
    date = models.DateTimeField(auto_now_add=True)  # used for displaying most recent first in creator profile
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
        # do I need the title returned to me? should I be returning the page code as something instead?


class Viewer(models.Model):
    """
    Class for viewer data.
    """
    viewer_creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="creator", default='')
    shown_name = models.CharField("My name (as it will appear to viewer)", max_length=100, default=viewer_creator)
    viewer_name = models.CharField(max_length=100)
    viewer_email = models.EmailField(max_length=100)


    def __str__(self):
        return self.viewer_name
