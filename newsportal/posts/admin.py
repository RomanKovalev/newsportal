from django.contrib import admin

from .models import Post, Comment

from django.utils.translation import ugettext_lazy as _


class PostAdmin(admin.ModelAdmin):

    fieldsets = (
        (None, {'fields': ('title', 'content', 'approved')}),
        # (_('Personal info'), {'fields': ('first_name', 'last_name', 'birth')}),
        # (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
        #                                'groups', 'user_permissions')}),
        # (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    # add_fieldsets = (
    #     (None, {
    #         'classes': ('wide',),
    #         'fields': ('email', 'password1', 'password2', 'birth'),
    #     }),
    # )
    list_display = ('title', 'owner', 'approved', 'created')
    # search_fields = ('email', 'first_name', 'last_name')
    ordering = ('created',)


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)