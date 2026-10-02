from django import forms
from django.core.validators import FileExtensionValidator

from .models import Comment, Meme


class MemeForm(forms.ModelForm):
    image = forms.FileField(
        label='Картинка або гіфка',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'gif', 'webp'])],
        help_text='Дозволені формати: JPG, PNG, GIF, WEBP',
    )

    class Meta:
        model = Meme
        fields = ['title', 'image']
        labels = {'title': 'Заголовок'}
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Наприклад: Коли код нарешті працює',
                'class': 'form-control',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        labels = {'text': 'Комментарий'}
        widgets = {
            'text': forms.Textarea(attrs={
                'placeholder': 'Напишите комментарий...',
                'rows': 2,
                'class': 'comment-input',
            }),
        }
