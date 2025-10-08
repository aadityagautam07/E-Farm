from django.db import models
from ckeditor.fields import RichTextField

# Create your models here.
class Contact_Mail(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    description = RichTextField()
    

    def __str__(self):
        return self.subject