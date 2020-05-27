from django.db import models
from django.shortcuts import reverse

from blog.models import Post

# Create your models here.
class Survey(models.Model):
    title = models.CharField(max_length=255)
    posts = models.ManyToManyField('blog.Post', blank=True, related_name='surveys')

    def get_update_url(self):
        return reverse('survey_update_url', kwargs={'id': self.id})

    def get_add_url(self):
        return reverse('survey_add_url', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('survey_delete_url', kwargs={'id': self.id})

    def get_result_url(self):
        return reverse('survey_result_url', kwargs={'id': self.id})

    def __str__(self):
        return self.title

    def get_options(self):
        return [option for option in self.options.all().values_list('title', flat=True)]

    class Meta:
        ordering = ['-id']

class Option(models.Model):
    title = models.CharField(max_length=255)
    count = models.IntegerField(default=0)
    survey = models.ForeignKey(
        Survey,
        related_name='options', on_delete=models.SET_NULL,
        null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-id']