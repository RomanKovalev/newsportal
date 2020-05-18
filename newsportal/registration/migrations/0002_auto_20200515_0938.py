from django.db import migrations

def move_backward(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    try:
        permission = Permission.objects.get(codename='can_approve')
        permission.delete()
    except Exception as e:
        print(e)
    try:
        group = Group.objects.get(name='Administrators')
        group.delete()
    except Exception as e:
        print(e)

    try:
        group = Group.objects.get(name='Editors')
        group.delete()
    except Exception as e:
        print(e)

    try:
        group = Group.objects.get(name='Users')
        group.delete()
    except Exception as e:
        print(e)                
    

def create_groups(apps, schema_editor):

    Group = apps.get_model('auth', 'Group')
    Permission = apps.get_model('auth', 'Permission')
    ContentType = apps.get_model('contenttypes', 'ContentType')

    try:
        content_type = ContentType.objects.get(app_label='auth', model='permission')
        permission = Permission.objects.create(codename='can_approve', name='Can change approve status', content_type=content_type)
        group, created = Group.objects.get_or_create(name='Administrators')
        group.permissions.add(permission)
        group, created = Group.objects.get_or_create(name='Editors')
        group.permissions.add(permission)
        group = Group.objects.get_or_create(name='Users')
    except Exception as e:
        print(e)
    

class Migration(migrations.Migration):

    operations = [
        migrations.RunPython(create_groups, move_backward),
    ]

    dependencies = [
        ('registration', '0001_initial'),
    ]