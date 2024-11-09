from django.contrib import admin

from .models import Author, Category, Tag, Article

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)


class TagsInline(admin.TabularInline):
    model = Article.tags.through


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [
        TagsInline,
    ]
    list_display = "pk", "title", "content", "pub_date", "author", "category"
    ordering = "pk",
    search_help_text = "title", "content", "author"

    def get_queryset(self, request):
        return (Article.objects.
                select_related("author").
                select_related("category").
                prefetch_related("tags")
                )

# admin.site.register(Article, ArticleAdmin)
