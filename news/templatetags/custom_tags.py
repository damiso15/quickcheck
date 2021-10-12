from news.models import Comment, Story
from django import template

register = template.Library()


@register.filter
def title(id):
    data = Story.objects.filter(story_id=id).first()
    if data:
        if data.types == 'comment':
            datas = Story.objects.filter(story_id=data.id).first()
            if datas:
                return datas.title
        return data.title
    else:
        return 'Story has not been fetched'


@register.filter
def url(id):
    data = Story.objects.filter(story_id=id).first()
    if data:
        if data.types == 'comment':
            datas = Story.objects.filter(story_id=data.id).first()
            if datas:
                return datas.get_absolute_url()
        return data.get_absolute_url()
    else:
        return '#'
