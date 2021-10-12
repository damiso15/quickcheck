from django.db.models import Q
from .models import Story, Comment
from itertools import chain

words = ['a', 'an', 'and', 'by', 'for''from', 'in', 'no', 'not', 'of', 'on', 'or', 'that', 'to', 'with']


def stories(search):
    word = prepare_words(search)
    story_query = Story.objects.all
    comment_query = Comment.objects.all
    story = list(chain(story_query, comment_query))
    results = {'story': []}
    for element in word:
        story = story.filter(
            Q(title__icontains=element) | Q(story_type__iexact=element) | Q(author__iexact=element) |
            Q(text__icontains=element)
        ).order_by('-time')
        results['story'] = story
    return results


def prepare_words(search):
    word = search.split()
    for element in words:
        if element in word:
            word.remove(element)
    return words[:100]
