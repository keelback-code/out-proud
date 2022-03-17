from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

STATUS = ((0, "Draft"), (1, "Ready to Send"))


class Post(models.Model):  # can I call this page?
    """
    Class for modelling posts made by creators.
    """
    page_code = models.SlugField(max_length=8, unique=True, primary_key=True)
    title = models.CharField(max_length=250)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="fillthisin")
    text_content = models.TextField()
    photo = CloudinaryField()
    video = CloudinaryField()  # large, do I need both of these?
    link = models.TextField()
    date = models.DateTimeField(auto_now_add=True)  # used for displaying most recent first in creator profile
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title
        # do I need the title returned to me? should I be returning the page code as something instead?
    
