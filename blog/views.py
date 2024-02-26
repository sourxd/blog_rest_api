from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PostSerializer, BlogSerializer, SubSerializer
from .models import Post, Blog, Subscription


class BlogAPIListView(generics.ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer


class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_queryset(self):
        blog_id = self.kwargs.get('blog_id', None)
        if blog_id:
            try:
                return Post.objects.filter(blog_id=blog_id)
            except Post.DoesNotExist:
                return None
        else:
            return Post.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'error': 'Неверный ID блога'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class PostAPIDetailView(APIView):

    def get(self, request, blog_id, pk):
        try:
            return Response(data=PostSerializer(Post.objects.get(blog_id=blog_id, pk=pk)).data,
                            status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Неверный ID блога или записи'}, status=status.HTTP_404_NOT_FOUND)


class PostCreateAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]


class PostEditAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.blog.user.id != request.user.id:
            return Response(data={'error': 'Вы не можете удалить данную запись'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(data={'message': 'Выбранная запись удалена'}, status=status.HTTP_204_NO_CONTENT)

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if instance.blog.user.id != request.user.id:
            return Response(data={'error': 'Вы не можете изменить данную запись'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class SubAPIView(generics.ListAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id', None)
        if user_id:
            try:
                return Subscription.objects.filter(subscriber_id=user_id)
            except Subscription.DoesNotExist:
                return None
        else:
            return Subscription.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if not queryset:
            return Response({'error': 'Подписок не найдено'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class SubAPIDetailView(generics.RetrieveAPIView,
                       generics.DestroyAPIView,
                       generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubSerializer
    lookup_field = 'blog_id'
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.subscriber.id != request.user.id:
            return Response(data={'error': 'Вы не можете удалить данную подписку'}, status=status.HTTP_403_FORBIDDEN)

        self.perform_destroy(instance)
        return Response(data={'message': 'Выбранная подписка удалена'}, status=status.HTTP_204_NO_CONTENT)

    def create(self, request, *args, **kwargs):
        field_value = request.data.get('blog')
        existing_record = Subscription.objects.filter(subscriber_id=request.user.id, blog=field_value).first()
        if existing_record:
            return Response({'error': 'Такая подписка уже существует'}, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request, *args, **kwargs)

class SubscriptionFeedAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        subscribed_blogs = Subscription.objects.filter(subscriber=user).values_list('blog', flat=True)
        return Post.objects.filter(blog__in=subscribed_blogs).order_by('-created_at')[:500]