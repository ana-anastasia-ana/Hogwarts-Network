from django.contrib import admin
from .models import User, Post, Like, Follow

class PostAdmin(admin.ModelAdmin):
    # Add any custom configurations for the Post model in the admin interface
    pass

admin.site.register(User)
admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Follow)
