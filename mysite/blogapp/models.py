from django.db import models


class Author(models.Model):
    class Meta:
        ordering = ["name"]

    name = models.CharField(max_length=100, db_index=True)
    bio = models.TextField(null=False, blank=True)

    def __str__(self):
        return f"Author (pk={self.pk}, name={self.name!r})"


class Category(models.Model):

    name = models.CharField(max_length=40, db_index=True)

    def __str__(self):
        return f"Category (pk={self.pk}, name={self.name!r})"


class Tag(models.Model):

    name = models.CharField(max_length=20, db_index=True)

    def __str__(self):
        return f"Tag (pk={self.pk}, name={self.name!r})"


class Article(models.Model):

    title = models.CharField(max_length=200, db_index=True)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, null=False, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, null=False, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, related_name="tags_name")

    def __str__(self):
        return f"Article (pk={self.pk}, title={self.title!r}, author={self.author.name!r})"
