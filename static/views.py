from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from .models import News
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
import urllib.request
import tempfile
from django.core.files import File


def base2(request):
    return render(request, 'blog/base2.html')

class BaseUser(ListView):
    model = News
    template_name = 'blog/base.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['username'] = self.request.user.username
        ctx['img_url'] = self.request.user.profile.img.url if hasattr(self.request.user, 'profile')\
                                                                    and self.request.user.profile.img else None
        return ctx


class ShowNewsView(ListView):
    model = News
    template_name = 'blog/home.html'
    context_object_name = 'news'
    ordering = ['-date']
    paginate_by = 5

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['title'] = 'Главная страница сайта'
        ctx['username'] = self.request.user.username
        return ctx


class UserALLNewsView(ListView):
    model = News
    template_name = 'blog/user_news.html'
    context_object_name = 'news'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return News.objects.filter(avtor=user).order_by('-date')

    def get_context_data(self, **kwargs):
        ctx = super(UserALLNewsView, self).get_context_data(**kwargs)

        ctx['title'] = f'Статьи от пользователя {self.kwargs.get("username")}'

        return ctx


class NewsDetailView(DetailView):
    model = News
    template_name = 'blog/news_detail.html'

    def get_context_data(self, **kwards):
        ctx = super(NewsDetailView, self).get_context_data(**kwards)

        ctx['title'] = News.objects.get(pk=self.kwargs['pk'])
        return ctx


class UpdateNewsView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title', 'text']

    def get_context_data(self, **kwargs):
        ctx = super(UpdateNewsView, self).get_context_data(**kwargs)

        ctx['title'] = 'Обновление статьи'
        ctx['btn_text'] = 'Обновить статью'
        return ctx

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True

        return False

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)


class DeleteNewsView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = News
    success_url = reverse_lazy('home')
    template_name = 'blog/delete_news.html'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.object = None

    def test_func(self):
        news = self.get_object()
        if self.request.user == news.avtor:
            return True

        return False

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(request, 'Статья успешно удалена')
        return HttpResponseRedirect(success_url)

    def get_success_url(self):
        return reverse_lazy('news-delete')

class CreateNewsView(LoginRequiredMixin, CreateView):
    model = News
    template_name = 'blog/create_news.html'

    fields = ['title', 'text']

    def get_context_data(self, **kwargs):
        ctx = super(CreateNewsView, self).get_context_data(**kwargs)

        ctx['title'] = 'Добавление статьи'
        ctx['btn_text'] = 'Добавить статью'
        return ctx

    def form_valid(self, form):
        form.instance.avtor = self.request.user
        return super().form_valid(form)


def contacts(request):
    return render(request, 'blog/contacts.html', {'title': 'Страница контакты'})
