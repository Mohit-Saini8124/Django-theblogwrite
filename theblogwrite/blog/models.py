from django.db import models
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from blog.utils import generate_unique_slug
from django.utils.text import slugify

from tinymce import HTMLField

# from ckeditor_uploader.fields import RichTextUploadingField

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Category(models.Model):
    title = models.CharField(max_length=20)

    def __str__(self):
        return self.title


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    

    def __str__(self):
        return self.user.username


class Post(models.Model):    
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    categories = models.ManyToManyField(Category)
    thumbnail = models.ImageField(upload_to = 'BlogHeadPostImages')
    content = HTMLField()# content = models.TextField()# content = RichTextUploadingField()#content = RichTextField() #content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    slug = models.SlugField(max_length=100, unique=True )


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.slug:
            if slugify(self.title) != self.slug:
                self.slug = generate_unique_slug(Post, self.title)
        else:
            self.slug = generate_unique_slug(Post, self.title)
        super(Post, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={
                                                'pk' : self.pk, 
                                                'slug': self.slug
                                            })

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')


    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()