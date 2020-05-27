from django.db import models
from django.utils.text import slugify
from django.shortcuts import reverse

from time import time


def generate_slug(title):
    new_slug = slugify(title, allow_unicode=True)
    return new_slug + '-' + str(int(time()))


class Post(models.Model):
    title = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True)
    body = models.TextField(blank=True, db_index=True)
    date_pub = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('post_detail_url', kwargs={'id': self.id})

    def get_update_url(self):
        return reverse('post_update_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('post_delete_url', kwargs={'id': self.id})

    def get_result_url(self):
        return reverse('post_result_url', kwargs={'id': self.id})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_slug(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-date_pub']