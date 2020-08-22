# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
# ---------------------------------------
# 1 - python -m pip install Pillow  
# ---------------------------------------

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default = 'default.jpg', upload_to = 'profile_images')
    website = models.URLField(null=True, blank=True, max_length=60)
    facebookid = models.CharField(null=True, blank=True, max_length=60)
    twitterid = models.CharField(null=True, blank=True, max_length=60)
    instagramid = models.CharField(null=True, blank=True, max_length=60)
    about_us = models.TextField(null=True, max_length=500, blank=True)
    hobbie = models.CharField(null=True, max_length=500, blank=True)
    

    def __str__(self):
        return f'{self.user.username}'

# When you are overriding model's save method in Django, you should also pass *args and **kwargs to overridden method.
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)
        if img.height > 250 or img.width > 245:
            output_size = (250, 245)
            img.thumbnail(output_size)
            img.save(self.image.path)