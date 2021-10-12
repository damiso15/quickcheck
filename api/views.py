from news.models import Story, Comment
from rest_framework import generics
from django.contrib.auth import get_user_model
from rest_framework import permissions
from django.template.defaultfilters import slugify
from django.utils import timezone
from .permissions import IsCreatorOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import CommentSerializer, StorySerializer, UserSerializer


@api_view(['GET'])
def api_root(request, formats=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=formats),
            'stories': reverse('story-list', request=request, format=formats),
            'comments': reverse('comment-list', request=request, format=formats),
        }
    )


class StoryList(generics.ListCreateAPIView):
    queryset = Story.objects.all().order_by('-time')
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'author']
    filter_fields = [
        'types',
        'author',
        'text',
    ]

    def perform_create(self, serializer):
        serializer.save(
            created_by=self.request.user,
            slug=slugify(self.request.data['title']),
            time=timezone.now(),
            author=self.request.user.username,
            score=0,
            story_type=self.request.data['types'].lower(),
        )


class StoryDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Story.objects.all()
    serializer_class = StorySerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]


class UserList(generics.ListAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


class CommentList(generics.ListAPIView):
    queryset = Comment.objects.select_related('parent_id').order_by('-time')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user.username, score=0)


class CommentDetail(generics.RetrieveAPIView):
    queryset = Comment.objects.select_related('parent_id').order_by('-time')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsCreatorOrReadOnly]
