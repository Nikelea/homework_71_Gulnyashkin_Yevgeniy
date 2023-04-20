from django.urls import path
from .views import IndexView, PublicationCreateView, PublicationView, like_publication

app_name = 'publications'

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('publications/create', PublicationCreateView.as_view(), name='create'),
    path('publications/<int:publication_pk>', PublicationView.as_view(), name='detail'),
    path('like/<int:pk>', like_publication, name='like_publication')
]

