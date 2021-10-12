from django.urls import path
from news import views

app_name = 'news'

urlpatterns = [
    path('', views.index, name='index'),
    path('story-detail/<uuid:id>/<slug:slug>/', views.story_detail, name='story_detail'),
    path('paginate/', views.paginate, name='paginate'),
    path('search-by-text/', views.search_by_text, name='search_by_text'),
    path('filter-by-types/', views.search_by_text, name='filter_by_types')
]
