from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsCreate, NewsUpdate, NewsDelete, subscriptions
)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsUpdate.as_view(), name='product_update'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='product_delete'),
    path('subscriptions/', subscriptions, name='subscriptions'),
]