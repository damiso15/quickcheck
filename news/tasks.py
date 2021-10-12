import requests
import datetime
import dateutil.parser
from celery import shared_task
from .models import Story, Comment
from django.template.defaultfilters import slugify

hacker_news_url = 'https://hacker-news.firebaseio.com/v0'


def get_item(id):
    item = requests.get(f'{hacker_news_url}/item/{id}.json')
    return item.json()


@shared_task
def get_and_store_comments(story_id, api_id):
    single_story = get_item(story_id)
    story = Story.objects.get(id=api_id, story_id=story_id)
    for element in single_story.get('kids', []):
        comments = get_item(element)
        comment, _ = Comment.objects.get_or_create(story_id=element, id=story.unique_id)
        comment.types = comments.get('type', '')
        comment.text = comment.get('text', '')
        comment.author = comments.get('by', '')
        comment.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(comments.get('time', 0)).strftime('%Y-%m-%d %H:%M:%S')
        )
        comment.parent_id = comments.get('parent', '')
        comment.save()


def get_latest_item_id():
    elements = requests.get(f'{hacker_news_url}/newstories.json')
    item = elements.json()
    latest_item_id = item[:10]
    return latest_item_id


@shared_task()
def store_stories():
    latest_item_id = get_latest_item_id()
    for element in reversed(latest_item_id):
        stories = get_item(element)
        story, _ = Story.objects.get_or_create (
            story_id=element,
            title=stories.get(
                'title', f"No title for this {stories.get('types', 'No type')} from the API"
            ),
        )
        story.types = stories.get('type', 'No type')
        story.url = stories.get('url', 'url')
        story.author = stories('by', 'No Author')
        story.slug = slugify(
            stories.get('title', f"No title for this {stories.get('type', 'No type')} from the API")
        )
        story.time = dateutil.parser.parse(
            datetime.datetime.fromtimestamp(stories.get('time', 0)).strftime("%Y-%m-%d %H:%M:%S")
        )
        story.descendants = stories.get('descendants', 0)
        story.score = stories.get('score', 0)
        story.save()
        get_and_store_comments.delay(story_id=story.story_id, api_id=story.unique_id)


@shared_task
def get_stories():
    store_stories.delay()
