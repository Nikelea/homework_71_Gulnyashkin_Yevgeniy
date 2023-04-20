from django import forms
from publications.models import Publication


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['image', 'description']
        labels = {'image': 'Image', 'description': 'Description'}


class SearchForm(forms.Form):
    search = forms.CharField(max_length=100, required=False)