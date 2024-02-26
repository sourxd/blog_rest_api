from rest_framework import serializers

from .models import Post, Blog, Subscription, User


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['blog']

    def create(self, validated_data):
        user = self.context['request'].user
        blog = Blog.objects.get(user=user)
        validated_data['blog'] = blog
        return super().create(validated_data)


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class SubSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'
        read_only_fields = ['subscriber']

    def create(self, validated_data):
        user = self.context['request'].user
        subscriber = User.objects.get(username=user)
        validated_data['subscriber'] = subscriber
        return super().create(validated_data)
