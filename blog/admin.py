from django.contrib import admin
from blog.models import Post, Tag, Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'text')
    readonly_fields = ['author', 'published_at']
    list_display = ['title', 'author', 'published_at']
    list_filter = ['tags']
    raw_id_fields = ['likes']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ('author', 'text')
    readonly_fields = ['published_at']
    list_display = ['author', 'post', 'published_at']
    # list_filter = ['author']
    raw_id_fields = ['author']

admin.site.register(Tag)
