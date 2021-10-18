from django.contrib import admin
from . import models

# Register your models here.

# admin.site.register(models.Type)


@admin.register(models.Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['story_id', 'display_types', 'title', 'url', 'author']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'types', 'author', 'local_author', 'story_id']
    list_per_page = 20
    list_filter = ('types',)


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['comment_id', 'title', 'author']
    list_per_page = 20

    def title(self, obj):
        return obj.story.title
    title.short_description = 'title'
