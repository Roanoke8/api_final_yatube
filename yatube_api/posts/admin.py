from django.contrib import admin

from .models import Comment, Post, Follow, Group


class PostAdmin(admin.ModelAdmin):
    list_display = ('pk', 'text', 'pub_date', 'author')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


admin.site.register(Post)
admin.site.register(Group)
admin.site.register(Comment)
admin.site.register(Follow)