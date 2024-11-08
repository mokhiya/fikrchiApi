from django.contrib import admin

from posts.models import PostModel


@admin.register(PostModel)
class PostModelAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')
    list_display_links = ('user', 'content')
    search_fields = ('user', 'content')

