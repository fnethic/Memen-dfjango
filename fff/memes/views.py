from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, MemeForm
from .models import Comment, Meme, MemeLike


def hippo_meme(request):
    recent_memes = Meme.objects.all().order_by('-created_at')[:6]
    return render(request, 'memes/hippo.html', {
        'title': 'Гіпопотам — мем для тебе',
        'subtitle': 'Коли код працює з першого разу',
        'memes': recent_memes,
        'comment_form': CommentForm(),
        'user': request.user,
    })


def all_memes(request):
    return render(request, 'memes/all_memes.html', {
        'memes': Meme.objects.all(),
        'comment_form': CommentForm(),
        'user': request.user,
    })


@login_required(login_url='login')
def toggle_like(request, meme_id):
    if request.method == 'POST':
        meme = get_object_or_404(Meme, id=meme_id)
        like, created = MemeLike.objects.get_or_create(meme=meme, user=request.user)
        if not created:
            like.delete()
    return redirect('memes:hippo_meme')


@login_required(login_url='login')
def add_comment(request, meme_id):
    meme = get_object_or_404(Meme, id=meme_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.meme = meme
            comment.user = request.user
            comment.save()
    return redirect('memes:hippo_meme')


@login_required(login_url='login')
def create_meme(request):
    if request.method == 'POST':
        form = MemeForm(request.POST, request.FILES)
        if form.is_valid():
            meme = form.save(commit=False)
            meme.created_by = request.user
            meme.save()
            return redirect('profile')
    else:
        form = MemeForm()

    return render(request, 'memes/create_meme.html', {
        'title': 'Створити мем',
        'form': form,
        'user': request.user,
    })
