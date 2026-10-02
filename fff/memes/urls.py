from django.urls import path

from .views import add_comment, all_memes, create_meme, hippo_meme, toggle_like

app_name = 'memes'

urlpatterns = [
    path('', hippo_meme, name='hippo_meme'),
    path('all/', all_memes, name='all_memes'),
    path('create/', create_meme, name='create_meme'),
    path('<int:meme_id>/like/', toggle_like, name='toggle_like'),
    path('<int:meme_id>/comment/', add_comment, name='add_comment'),
]
