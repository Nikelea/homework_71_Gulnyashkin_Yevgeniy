from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, reverse
from django.utils.http import urlencode
from django.views.generic import View, TemplateView, CreateView, DetailView, ListView, UpdateView
from django.contrib.auth.models import User
from accounts.forms import RegistrationForm, ProfileRegistrationForm
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from accounts.models import Profile, Sex, Follower
from accounts.helpers import SearchView
from publications.forms import SearchForm


class LoginView(View):
    def get(self, request, *args, **kwargs):
        next_path = request.GET.get('next')
        return render(request, 'registration/login.html', {
        'next_path': next_path
    })

    def post(self, request, *args, **kwargs):
        if request.POST.get('username'):
            username = request.POST.get('username')
            password = request.POST.get('password')
            next_path = request.POST.get('next')
            user = authenticate(request, username=username, password=password)
        elif request.POST.get('email'):
            email = request.POST.get('email')
            user = get_user_model().objects.get(email=email)
            username = user.username
            password = request.POST.get('password')
            next_path = request.POST.get('next')
            user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if next_path:
                return redirect(next_path)
            return redirect('publications:index')
        return render(request, 'registration/login.html', {'has_error': True})


class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return redirect('publications:index')


class RegisterView(View):
    form_class = RegistrationForm
    template_name = 'registration/register.html'

    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        profile_form = ProfileRegistrationForm()
        return render(request, self.template_name, context={'form': form, 'profile_form': profile_form})

    def post(self, request, *args, **kwargs):
        form_kwargs = {}
        if request.method == 'POST':
            form = RegistrationForm(data=request.POST)
            form_kwargs['data'] = request.POST
            form_kwargs['files'] = request.FILES
            profile_form = ProfileRegistrationForm(**form_kwargs)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            form_kwargs = {'instance': user.profile}
            form_kwargs['data'] = request.POST
            form_kwargs['files'] = request.FILES
            profile_form = ProfileRegistrationForm(**form_kwargs)
            profile = profile_form.save()
            login(request, user)
            return redirect('accounts:profile', user.pk)
        else:
            form = RegistrationForm(data=request.POST)
            form_kwargs['data'] = request.POST
            form_kwargs['files'] = request.FILES
            profile_form = ProfileRegistrationForm(**form_kwargs)
        return render(request, self.template_name, context={'form': form, 'profile_form': profile_form})


class UserListView(SearchView):
    context_object_name = 'users'
    model = get_user_model()
    template_name = 'user_list.html'
    ordering = ['-date_joined']
    search_fields = {
        'first_name': 'icontains',
        'last_name': 'icontains'
    }
    search_form = SearchForm

    def get_search_form(self):
        return SearchForm(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserListView, self).get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({
                'search': self.search_value
            })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value:
            query = Q(first_name__icontains=self.search_value) | Q(last_name__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset


class ProfileView(DetailView):
    template_name = 'profile.html'
    model = get_user_model()
    pk_url_kwarg = 'user_pk'


    def get_context_data(self, **kwargs):
        followers = Follower.objects.filter(user=self.request.user)
        context = super().get_context_data(**kwargs)
        context.update({ 'followers': followers })
        return context


def follow_user(request, user_pk):
    followers =Follower.objects.filter(user__pk=request.user.pk).filter(follow=user_pk)
    if followers:
        for follower in followers:
            follower.delete()
            user= get_object_or_404(get_user_model(), pk=request.user.pk)
            user.profile.subscriptions_counter -= 1
    else:
        user= get_object_or_404(get_user_model(), pk=request.user.pk)
        Follower.objects.create(user=user, follow= get_object_or_404(get_user_model(),pk=user_pk))
        user.profile.subscriptions_counter += 1

    user.save()
    return redirect('accounts:profile', user_pk)

