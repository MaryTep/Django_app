from django.shortcuts import render

from django.views.generic import (ListView)

from blogapp.models import Article


class ArticleListView(ListView):
    template_name = 'blogapp/articles_list.html'
    context_object_name = "article"
    queryset = (
                Article.objects.defer("content").
                select_related("author").
                select_related("category").
                prefetch_related("tags")
                )
