from django import template
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ObjectDoesNotExist

register = template.Library()

@register.filter(name='has_permission')
def has_permission(group_name, permission):
    try:
        group = Group.objects.get(name=group_name)
        permission = Permission.objects.get(codename=permission)
    except ObjectDoesNotExist: 
        return False
    return True if permission in group.permissions.all() else False