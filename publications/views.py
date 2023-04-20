from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View, TemplateView, FormView, ListView, DetailView, CreateView, DeleteView
from django.contrib.auth import get_user_model
from publications.models import Publication
from publications.forms import PublicationForm


def like_publication(request, pk):
    publication = get_object_or_404(Publication, id=request.POST.get('publication_id'))
    if request.user in publication.likes.all():
        publication.likes.remove(request.user)
        publication.likes_counter = publication.likes.count()
    else:
        publication.likes.add(request.user)
        publication.likes_counter = publication.likes.count()
    publication.save()
    return HttpResponseRedirect(reverse('publications:detail', args=[str(pk)]))


class IndexView(ListView):
    context_object_name = 'publications'
    model = Publication
    template_name = 'publication/publication_list.html'


class PublicationCreateView(CreateView):
    model = Publication
    form_class = PublicationForm
    template_name = 'publication/create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['user'] = self.request.user
        return context

    def form_valid(self, form):
        user = get_object_or_404(get_user_model(), pk=self.request.user.pk)
        publication = form.save(commit=False)
        publication.user = user
        print(publication)
        publication.save()
        return redirect('publications:index')
                        # publication_pk=publication.pk)


class PublicationView(DetailView):
    template_name = 'publication/publication.html'
    model = Publication
    pk_url_kwarg = 'publication_pk'


