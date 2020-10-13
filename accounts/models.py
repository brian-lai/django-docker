from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Organization(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, max_length=255)
    description = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    creator = models.TextField()


    def get_absolute_url(self):
        return reverse('organization_detail', args=[self.slug])

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(Organization, self).save(*args, **kwargs)


    class Meta:
        ordering = ['created_on']

        def __unicode__(self):
            return self.name