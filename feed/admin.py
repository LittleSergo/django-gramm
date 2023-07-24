from django.contrib import admin

from .models import User, Image, Post, Comment


class UserAdmin(admin.ModelAdmin):
    """Representation for User model in admin site."""
    fieldsets = [
        ('User info', {'fields': [
            'profile_image', 'username', 'password', 'first_name',
            'last_name', 'email', 'bio', 'followers',
        ]}),
        ('Dates', {'fields': [
            'date_joined', 'last_login',
        ]}),
        ('Statuses', {'fields': [
            'is_active', 'is_superuser', 'is_staff',
        ]})
    ]
    readonly_fields = ('password', 'date_joined', 'last_login',)


class ImageInLine(admin.TabularInline):
    model = Image
    extra = 1


class CommentInLine(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [ImageInLine, CommentInLine]


admin.site.register(User, UserAdmin)
admin.site.register(Post, PostAdmin)
