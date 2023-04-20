from typing import Dict
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.http import urlencode
from django.views import View
from django.views.generic import FormView as DjangoFormView, ListView


class SearchView(ListView):
    template_name = None
    model = None
    ordering = None
    context_object_name = None
    paginate_by = 5
    paginate_orphans = 2
    search_form = None
    search_fields: Dict[str, str] = {}

    def get_search_form(self):
        return self.search_form(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get('search')

    def get(self, request, *args, **kwargs):
        self.form = self.get_search_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form
        if self.search_value:
            context['query'] = urlencode({
                'search': self.search_value
            })
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        print(queryset)
        if self.search_value:
            query = Q()
            query_list = [
                Q(**{f'{key}__{value}': self.search_fields})
                for key, value in self.search_fields.items()
            ]
            for query_part in query_list:
                query = (query | query_part)
            print(query)
            queryset = queryset.filter(query)
        return queryset

