# from django.test import TestCase

# Create your tests here.
from cgitb import html
import requests
import json


# response_API = requests.get('https://hacker-news.firebaseio.com/v0/28819131.json?print=pretty')
# print(response_API.status_code)
# data = response_API.text
# parse_json = json.loads(data)
# print(parse_json)

# import requests
# import json
#
# response_API = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
# print(response_API.status_code)
# data = response_API.text
# parse_json = json.loads(data)
# print(parse_json)


# from hackernews import HackerNews
# hn = HackerNews()
# top_story_ids = hn.top_stories()
# print(top_story_ids)

# from hn import HN
#
# hn = HN()
#
# story = hn.get_stories(story_type='newest', limit=1)
# print(story)

hacker_news_url = 'https://hacker-news.firebaseio.com/v0'


# def get_latest_item_id():
#     elements = requests.get(f'{hacker_news_url}/newstories.json')
#     item = elements.json()
#     latest_item_id = item[:10]
#     return latest_item_id

def get_item(id):
    items = requests.get(f'{hacker_news_url}/item/{id}.json')
    return items.json()


elements = requests.get(f'{hacker_news_url}/newstories.json')
item = elements.json()
latest_item_id = item[:10]
for i in reversed(latest_item_id):
    respond = get_item(i)
    print(respond)
