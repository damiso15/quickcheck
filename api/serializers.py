from news.models import Story, Comment
from django.contrib.auth import get_user_model
from rest_framework import serializers


class StorySerializer(serializers.HyperlinkedModelSerializer):
    created_by = serializers.ReadOnlyField(source='created_by.username')
    author = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()
    descendants = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()
    slug = serializers.ReadOnlyField()

    class Meta:
        model = Story
        fields = ['unique_id', 'types', 'title', 'url', 'author', 'created_by', 'slug', 'time', 'descendants', 'score']


class UserSerializer(serializers.ModelSerializer):
    stories = serializers.HyperlinkedRelatedField(many=True, view_name='user-detail', read_only=True)

    class Meta:
        model = get_user_model()
        fields = ['url', 'id', 'username', 'stories']


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    story = serializers.SlugRelatedField(slug_field="unique_id", queryset=Story.objects.all())
    author = serializers.ReadOnlyField()
    score = serializers.ReadOnlyField()
    time = serializers.ReadOnlyField()

    class Meta:
        model = Comment
        fields = ['unique_id', 'types', 'text', 'author', 'time', 'parent_id']
