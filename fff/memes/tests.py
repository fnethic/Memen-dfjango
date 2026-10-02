from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase

from .models import Comment, Meme, MemeLike


class MemeCreationTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='alice',
            password='StrongPass123!'
        )

    def test_profile_requires_login(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

    def test_user_can_create_meme(self):
        self.client.login(username='alice', password='StrongPass123!')

        gif = SimpleUploadedFile(
            'test.gif',
            b'GIF89a\x01\x00\x01\x00\x80\x00\x00\x00\x00\x00\xff\xff\xff!',
            content_type='image/gif',
        )

        response = self.client.post('/memes/create/', {
            'title': 'Мій перший мем',
            'image': gif,
        })

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Meme.objects.filter(title='Мій перший мем').exists())

    def test_user_can_toggle_meme_like(self):
        meme = Meme.objects.create(
            title='Мем для лайка',
            image=SimpleUploadedFile('like.gif', b'GIF89a', content_type='image/gif'),
            created_by=self.user,
        )
        self.client.login(username='alice', password='StrongPass123!')

        response = self.client.post(f'/memes/{meme.id}/like/')
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MemeLike.objects.filter(meme=meme, user=self.user).exists())

        self.client.post(f'/memes/{meme.id}/like/')
        self.assertFalse(MemeLike.objects.filter(meme=meme, user=self.user).exists())

    def test_user_can_comment_on_meme(self):
        meme = Meme.objects.create(
            title='Мем для комментария',
            image=SimpleUploadedFile('comment.gif', b'GIF89a', content_type='image/gif'),
            created_by=self.user,
        )
        self.client.login(username='alice', password='StrongPass123!')

        response = self.client.post(f'/memes/{meme.id}/comment/', {'text': 'Смешно!'})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Comment.objects.filter(meme=meme, user=self.user, text='Смешно!').exists())

    def test_guest_cannot_like_or_comment(self):
        meme = Meme.objects.create(
            title='Закрытый мем',
            image=SimpleUploadedFile('guest.gif', b'GIF89a', content_type='image/gif'),
            created_by=self.user,
        )

        like_response = self.client.post(f'/memes/{meme.id}/like/')
        comment_response = self.client.post(f'/memes/{meme.id}/comment/', {'text': 'Гость'})

        self.assertEqual(like_response.status_code, 302)
        self.assertEqual(comment_response.status_code, 302)
        self.assertFalse(MemeLike.objects.filter(meme=meme).exists())
        self.assertFalse(Comment.objects.filter(meme=meme).exists())
