from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class OurTeam(models.Model):
    first_name = models.CharField(max_length=255, null=True, blank=True)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField()
    designation = models.CharField(max_length=255)
    twitter_link = models.CharField(max_length=255, null=True, blank=True)
    fb_link = models.CharField(max_length=255, null=True, blank=True)
    linkedin_link = models.CharField(max_length=255, null=True, blank=True)
    youtube_link = models.CharField(max_length=255, null=True, blank=True)
    your_photo = models.ImageField(upload_to="media/webpages_content/team/%Y-%m-%d/")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.first_name

class LatestBlog(models.Model):
    image = models.ImageField(upload_to="media/webpages_content/latest_Blogs/%Y-%m-%d/")
    title = models.CharField(max_length=255)
    description = RichTextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class HomeSlider(models.Model):
    title = models.CharField(max_length=255)
    description = RichTextField()
    btn_text = models.CharField(max_length=255)
    # btn_link = models.CharField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="media/webpages_content/HomeSlider/%Y-%m-%d/")
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title