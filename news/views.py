from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Comment, Story
from django.http import JsonResponse
from django.template import loader
from .search import stories, prepare_words
from itertools import chain

# Create your views here.


def index(request):
    story = Story.objects.all().order_by('-time')[:4]
    typ = Story.objects.order_by('-types').values_list('types')
    types = []
    for element in typ:
        if element[0] in types:
            continue
        types.append(element[0])
    context = {
        'page_title': 'WELCOME TO NEWS CENTRAL',
        'story': story,
        'types': types
    }
    return render(request, 'news/index.html', context)


def story_detail(request, id, slug):
    story = get_object_or_404(Story, unique_id=id, slug=slug)
    comments_by = get_object_or_404(Comment).filter(story_id=Comment.parent_id)
    comments = Comment.objects.select_related('parent_id').filter(parent_id=story, text=story)
    main_comment = list(chain(comments_by, comments))
    context = {
        'page_title': f'{story.title}',
        'story': story,
        'main_comment': main_comment
    }
    return render(request, 'news/detail.html', context)


def paginate(requests):
    stories_paginate = Story.objects.all().order_by('-time')
    page = requests.POST.get('page')
    result_per_page = 20
    paginator = Paginator(stories_paginate, result_per_page)
    try:
        stories_paginate = paginator.page(page)
    except PageNotAnInteger:
        stories_paginate = paginator.page(2)
    except EmptyPage:
        stories_paginate = paginator.page(paginator.num_pages)
    stories_html = loader.render_to_string('news/stories.html', {'stories_paginate': stories_paginate})
    output_data = {
        'stories.html': stories_html,
        'has_next': stories_paginate.has_next(),
        'stories_count': len(stories_paginate)
    }
    return JsonResponse(output_data)


def search_by_text(request):
    if request.method == 'POST':
        search_text = request.POST.get('search')
        stories_search = stories(search_text).get('stories', [])
        if len(stories_search) > 10:
            page = request.POST.get('page')
            results_per_page = 10
            paginator = Paginator(stories_search, results_per_page)
            try:
                stories_search = paginator.page(page)
            except PageNotAnInteger:
                stories_search = paginator.page(2)
            except EmptyPage:
                stories_search = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string('news/stories.html', {'stories_search': stories_search})
            stories_list = []
            for element in stories_search:
                stories_list.append({'title': element.title, 'author': element.author, 'type': element.types,
                                     'text': element.text})
            output_data = {
                'stories_html': stories_html,
                'has_next': stories_search.has_next(),
                'stories_count': len(stories_search),
            }
            return JsonResponse(output_data)
        elif len(stories_search) < 10 and len(stories_search) > 10:
            stories_html = loader.render_to_string('news/stories.html', {'stories_search': stories_search})
            stories_list = []
            for element in stories_search:
                stories_list.append({'title': element.title, 'author': element.author, 'type': element.types,
                                     'text': element.text})
            output_data = {
                'stories_html': stories_html,
                'has_next': False,
                'stories_count': len(stories_search),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({'no_story': True})

    elif request.method == 'GET':
        search_text = request.GET.get('search')
        stories_search = stories(search_text).get('stories', [])
        if len(stories_search) > 10:
            page = request.POST.get('page')
            results_per_page = 10
            paginator = Paginator(stories_search, results_per_page)
            try:
                stories_search = paginator.page(page)
            except PageNotAnInteger:
                stories_search = paginator.page(1)
            except EmptyPage:
                stories_search = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string('news/stories.html', {'stories_search': stories_search})
            stories_list = []
            for element in stories_search:
                stories_list.append({'title': element.title, 'author': element.author, 'type': element.types,
                                     'text': element.text})
            output_data = {
                'stories_html': stories_html,
                'has_next': stories_search.has_next(),
                'stories_count': len(stories_search),
            }
            return JsonResponse(output_data)
        elif len(stories_search) < 10 and len(stories_search) > 10:
            stories_html = loader.render_to_string('news/stories.html', {'stories_search': stories_search})
            stories_list = []
            for element in stories_search:
                stories_list.append({'title': element.title, 'author': element.author, 'type': element.types,
                                     'text': element.text})
            output_data = {
                'stories_html': stories_html,
                'has_next': False,
                'stories_count': len(stories_search),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({'no_story': True})


def filter_by_types(request):
    if request.method == 'POST':
        types = request.POST['types']
        stories_filter = Story.objects.filter(types=types).order_by('-time')
        if len(stories_filter) > 10:
            page = request.POST.get('page')
            results_per_page = 10
            paginator = Paginator(stories_filter, results_per_page)
            try:
                stories_filter = paginator.page(page)
            except PageNotAnInteger:
                stories_filter = paginator.page(1)
            except EmptyPage:
                stories_filter = paginator.page(paginator.num_pages)
            stories_html = loader.render_to_string('news/stories.html', {'stories_filter': stories_filter})
            output_data = {
                'stories_html': stories_html,
                'has_next': stories_filter.has_next(),
                'stories_count': len(stories_filter),
            }
            return JsonResponse(output_data)
        elif len(stories_filter) < 10 and len(stories_filter) > 10:
            stories_html = loader.render_to_string('news/stories.html', {'stories_filter': stories_filter})
            output_data = {
                'stories_html': stories_html,
                'has_next': False,
                'stories_count': len(stories_filter),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({'no_story': True})

    elif request.method == 'GET':
        types = request.GET['types']
        stories_filter = Story.objects.filter(types=types).order_by('-time')
        if len(stories_filter) > 10:
            page = request.GET.get('page')
            results_per_page = 10
            paginator = Paginator(stories_filter, results_per_page)
            try:
                stories_filter = paginator.page(page)
            except PageNotAnInteger:
                stories_filter = paginator.page(1)
            except EmptyPage:
                stories_filter = paginator.page(paginator.num_pages)
            new_stories_html = loader.render_to_string('news/stories.html', {'stories_filter': stories_filter})
            output_data = {
                'new_stories_html': new_stories_html,
                'new_has_next': stories_filter.has_next(),
                'new_stories_count': len(stories_filter),
            }
            return JsonResponse(output_data)
        elif len(stories_filter) < 10 and len(stories_filter) > 10:
            new_stories_html = loader.render_to_string('news/stories.html', {'stories_filter': stories_filter})
            output_data = {
                'new_stories_html': new_stories_html,
                'new_has_next': False,
                'new_stories_count': len(stories_filter),
            }
            return JsonResponse(output_data)
        else:
            return JsonResponse({'no_story': True})
