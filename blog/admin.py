from django.contrib import admin
from .models import Post, PostSetting , Category, LikeComment, Comment
# Register your models here.

admin.site.register(Post)
admin.site.register(Category)
admin.site.register(LikeComment)

#admin.site.register(Comment)
#admin.site.register(LikeComment)

@admin.register(Comment)
#for register Comment model as class
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'text', 'created_date', 'update_date', 'is_confirmed')
    list_filter = ('is_confirmed', 'created_date', 'author')
    search_fields = ('post', 'author', 'text', 'created_date', 'update_date', 'is_confirmed')
    actions = ('approve_comments')

    def approve_comments(self, request, queryset):
    #Finally, we have the actions method this will help us for approving 
    #many comment objects at once, the approve_comments method is a simple 
    #function that takes a queryset and updates the active boolean field to True.
        queryset.update(is_confirmed=True)

class PostSettingInline(admin.TabularInline):
    model = PostSetting