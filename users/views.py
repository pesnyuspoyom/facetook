from django.shortcuts import render, redirect
# from django.contrib.auth.forms import UserCreationForm
from .forms import UserRegisterForm, ProfileImageForm, UserUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def register(request):
    error = ''
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Пользовать {username} был успешно создан!')
            return redirect('home')
        else:
            error = "Форма заполнена неправильно"

    form = UserRegisterForm()

    data = {
        'title':'Страница регистрации',
        'form': form,
        "error": error,
    }

    return render(request, 'users/registration.html', data)


@login_required
def profile(request):
    if request.method == 'POST':
        profileForm = ProfileImageForm(request.POST, request.FILES, instance=request.user.profile)
        updateUserForm = UserUpdateForm(request.POST, instance=request.user)
        
        if profileForm.is_valid() and updateUserForm.is_valid():
            updateUserForm.save()
            profileForm.save()
            messages.success(request, f'Профиль был успешно обновлен!')
            return redirect('profile')
    else:
        profileForm = ProfileImageForm(instance=request.user.profile)
        updateUserForm = UserUpdateForm(instance=request.user)

    data = {
        'profileForm': profileForm,
        'updateUserForm': updateUserForm
    }

    return render(request, 'users/profile.html', data)


# Create your views here.