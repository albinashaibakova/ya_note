from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from notes.models import Note


User = get_user_model()


class TestHomePage(TestCase):

    HOME_URL = reverse('notes:list')


    @classmethod
    def setUpTestData(cls):
        all_notes = []
        cls.author = User.objects.create(username='Автор заметки')
        for index in range(settings.NOTES_COUNT_ON_HOME_PAGE + 1):
            
            notes = Note(title=f'Заметка {index}',
                         text='Текст заметки',
                         slug=f'slug{index}',
                         author=cls.author)
            all_notes.append(notes)
        Note.objects.bulk_create(all_notes)
        print(Note.objects.all())

    def test_new_count(self):
        self.client.force_login(self.author)
        response = self.client.get(self.HOME_URL)
        object_list = response.context['object_list']
        notes_count = object_list.count()
        self.assertEqual(notes_count, settings.NOTES_COUNT_ON_HOME_PAGE)
