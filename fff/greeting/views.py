from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def home(request):
    return render(request, 'greeting/index.html', {
        'title': 'Ласкаво просимо',
        'message': 'Привіт! Ти на головній сторінці проекту.',
        'user': request.user,
    })


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'greeting/register.html', {
        'title': 'Реєстрація',
        'form': form,
    })


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('profile')
    else:
        form = AuthenticationForm()

    return render(request, 'greeting/login.html', {
        'title': 'Вхід',
        'form': form,
    })


def logout_view(request):
    logout(request)
    return render(request, 'greeting/logout.html', {
        'title': 'Ви вийшли з акаунта',
        'message': 'Ви успішно вийшли з акаунта. До нових зустрічей!',
    })


@login_required(login_url='login')
def profile(request):
    user_memes = request.user.memes.all().order_by('-created_at')
    return render(request, 'greeting/profile.html', {
        'title': 'Профіль',
        'user': request.user,
        'memes': user_memes,
    })
