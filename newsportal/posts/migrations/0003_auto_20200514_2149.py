# Generated by Django 3.0.6 on 2020-05-14 21:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200514_1211'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='post',
            options={'permissions': [('change_approved_status', 'Can change approved or not')]},
        ),
    ]
