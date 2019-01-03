from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse

from catalog.models import Author


class RenewBookInstancesViewTest(TestCase):
    def setUp(self):
        # Create two users
        test_user1 = User.objects.create_user(username="rodmunch", password='SeKrItPaSs')
        test_user2 = User.objects.create_user(username="bendover", password='SeKrItPaSs')

        test_user1.save()
        test_user2.save()

        # Add permissions
        permission = Permission.objects.get(name='Set book as returned')
        test_user2.user_permissions.add(permission)
        test_user2.save()

        # Create an author
        test_author = Author.objects.create(first_name='John', last_name='Smith')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('catalog:author_create'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith('/accounts/login/'))

    def test_redirect_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username="rodmunch", password='SeKrItPaSs')
        response = self.client.get(reverse('catalog:author_create'))
        self.assertEqual(response.status_code, 403)

    def test_uses_correct_template(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.get(reverse('catalog:author_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'catalog/author_form.html')

    def test_create_author(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.post(reverse('catalog:author_create'), data={
            'first_name': 'Turtle',
            'last_name': 'Newman',
            'date_of_birth': '10/03/1969'
        })
        self.assertEqual(response.status_code, 302)

    def test_fail_to_create_author_no_first_name(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.post(reverse('catalog:author_create'), data={
            'last_name': 'Newman',
            'date_of_birth': '10/03/1969'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')

    def test_fail_to_create_author_no_last_name(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.post(reverse('catalog:author_create'), data={
            'first_name': 'Mean Gene',
            'date_of_birth': '10/03/1969'
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')

    def test_fail_to_create_author_no_data(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.post(reverse('catalog:author_create'), data={
        })
        self.assertEqual(response.status_code, 200)
        self.assertFormError(response, 'form', 'first_name', 'This field is required.')
        self.assertFormError(response, 'form', 'last_name', 'This field is required.')

    def test_default_date_of_death_label(self):
        login = self.client.login(username="bendover", password='SeKrItPaSs')
        response = self.client.get(reverse('catalog:author_create'))
        self.assertContains(response, '12/10/2016')
