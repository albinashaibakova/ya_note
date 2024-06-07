from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from unittest import skip

from notes.models import Note

User = get_user_model()


class TestRoutes(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.note = Note.objects.create(title='Заголовок',
                                       text='Текст',
                                       slug='Slug',
                                       author = User.objects.create(username='Автор заметки'))
        cls.reader = User.objects.create(username='Читатель')

    def test_page_availability(self):

        
        urls = (
            ('notes:home', None),
            ('notes:detail', (self.note.slug,)),
            ('yanote:login', None),
            ('yanote:logout', None),
            ('yanote:signup', None),
        )
    

        for name, args in urls:
            with self.subTest(name=name):
                url = reverse(name, args=args)
                response = self.client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_page_availability_for_edit_and_delete_note(self):
        users_statuses = (
                (self.author, HTTPStatus.OK),
                (self.reader, HTTPStatus.NOT_FOUND),
            )
        for user, status in users_statuses:
            self.client.force_login(user)
            for name in ('notes:edit', 'notes:delete'):
                with self.subTest(user=user, name=name):
                    url = reverse(name, args=(self.note.id,))
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status)





    @skip
    def test_home_page(self):
        """Tests homepage is available for anonymous users"""
        url = reverse('notes:home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)

    @skip
    def test_note_detail_page(self):
        """Tests note detail page"""
        url = reverse('notes:detail', args=(self.note.slug,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, HTTPStatus.OK)