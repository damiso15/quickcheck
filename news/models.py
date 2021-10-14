from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model
import uuid

# Create your models here.


class Type(models.Model):
    name = models.CharField(max_length=15, help_text='Enter a Type (e.g. Story, Comments, etc)', null=False, default='No type')

    def __str__(self):
        return self.name


class Story(models.Model):
    unique_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    story_id = models.IntegerField('Story ID', null=True)
    types = models.ManyToManyField(Type, help_text='Pick a Type or Create a new Type')
    title = models.TextField('Story Title', null=False)
    url = models.URLField('Story URL', null=True)
    author = models.CharField('Story Author', max_length=50, null=True)
    created_by = models.ForeignKey(get_user_model(), related_name='stories', on_delete=models.CASCADE, null=True)
    slug = models.SlugField(max_length=500, null=True)
    time = models.DateTimeField('Date Story was created', null=True)
    descendants = models.IntegerField('The total comments counted', null=True)
    score = models.IntegerField("Story's score or the votes of a pollopt", null=True)

    class Meta:
        ordering = ['title', 'author']
        verbose_name = 'Story'
        verbose_name_plural = 'Stories'

    def display_types(self):
        return ', '.join([types.name for types in self.types.all()[:3]])
    display_types.short_description = 'Types'

    def get_absolute_url(self):
        return reverse('story-detail', args=[str(self.unique_id), self.slug])

    def __str__(self):
        return self.title


class Comment(models.Model):
    unique_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    comment_id = models.IntegerField('Comment ID', null=True, unique=True)
    types = models.ManyToManyField(Type, help_text='Pick a Type or Create a new Type')
    text = models.TextField('The Comment', null=False)
    author = models.CharField('Comment Author', max_length=50, null=True)
    time = models.DateTimeField('Date Comment was created', null=True)
    parent_id = models.ForeignKey(Story, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def display_types(self):
        return ', '.join([types.name for types in self.types.all()[:3]])
    display_types.short_description = 'Type'

    def __str__(self):
        return self.parent_id.title
