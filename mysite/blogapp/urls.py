from django.urls import path, include

from .views import (
                    ArticleListView,
)

app_mame = 'blogapp'

urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='articles_list'),
]

