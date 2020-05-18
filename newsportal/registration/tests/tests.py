from datetime import datetime

from django.test import TestCase, TransactionTestCase
from django.shortcuts import reverse
from django.contrib.auth.models import Group, Permission, ContentType
from django.contrib.auth import get_user_model

from newsportal.posts.models import Post


class SignUpPageTests(TransactionTestCase):

    def setUp(self) -> None:
        self.email = 'testuser1@email.com'
        self.email_global = 'testuser@email.com'
        self.birth = '2020-05-18'
        self.password = 'password'
        self.first_name = 'First Name'
        self.last_name = 'Last Name'
        self.title = 'Some title'
        self.content = 'Some content'

        content_type = ContentType.objects.get(app_label='auth', model='permission')
        permission = Permission.objects.create(codename='can_approve', name='Can change approve status', content_type=content_type)
        group, created = Group.objects.get_or_create(name='Administrators')
        group.permissions.add(permission)
        group, created = Group.objects.get_or_create(name='Editors')
        group.permissions.add(permission)
        self.group, created = Group.objects.get_or_create(name='Users')
        User = get_user_model()
        self.user = User.objects.create(
            email = self.email_global,
            birth = self.birth,
            password = self.password,
            first_name = self.first_name,
            last_name = self.last_name,
        )
        self.user.set_password(self.password)
        self.user.groups.add(group)
        self.user.save()

    def test_signup_page_url(self):
        response = self.client.get("/signup/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_page_view_name(self):
        response = self.client.get(reverse('registration:signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, template_name='registration/signup.html')

    def test_signup_form(self):
        response = self.client.post(reverse('registration:signup'), data={
            'email': self.email,
            'birth': self.birth,
            'password1': self.password,
            'password2': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
        })
        self.assertEqual(response.status_code, 200)

        User = get_user_model()
        
        users = User.objects.all()
        self.assertEqual(users.count(), 2)

        user = User.objects.get(email=self.email)
        
        self.assertEqual(user.groups.all().count(), 1)
        self.assertEqual(user.groups.all()[0].name, self.group.name)
        self.assertEqual(user.email, self.email)
        self.assertEqual(user.birth.strftime('%Y-%m-%d'), self.birth)
        self.assertEqual(user.first_name, self.first_name)
        self.assertEqual(user.last_name, self.last_name)





    

