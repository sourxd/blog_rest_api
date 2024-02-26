from django.contrib import admin
from django.urls import path

from blog.views import BlogAPIListView, PostAPIView, PostAPIDetailView, PostCreateAPIView, PostEditAPIView, SubAPIView, \
    SubAPIDetailView, SubscriptionFeedAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/bloglist/', BlogAPIListView.as_view()), # список блогов
    path('api/v1/posts/<int:blog_id>/', PostAPIView.as_view()), # все записи в блоге по id блога
    path('api/v1/posts/<int:blog_id>/<int:pk>/', PostAPIDetailView.as_view()), # запись по id блога и id записи
    path('api/v1/newpost/', PostCreateAPIView.as_view()), # создание новой записи
    path('api/v1/editpost/<int:pk>/', PostEditAPIView.as_view()), # редактирование/удаление записи
    path('api/v1/sub/<int:user_id>/', SubAPIView.as_view()), # просмотр подписок по id пользователя
    path('api/v1/sub/<int:user_id>/<int:blog_id>/', SubAPIDetailView.as_view()), # создание/удаление подписки
    path('api/v1/newsfeed/', SubscriptionFeedAPIView.as_view()), # лента последних постов
]
