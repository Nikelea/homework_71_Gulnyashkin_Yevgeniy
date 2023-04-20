from django.urls import include, path
from rest_framework import routers
from api_v2 import views
from api_v2.views import LogoutView, PubViewSet, PubListView, PubDetailView
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'publications', views.PubViewSet)

app_name = 'api_v2'

urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('login/', obtain_auth_token, name='api_token_auth'),
    path('like/<int:pk>', PubViewSet.as_view({'get': 'like_it'}), name='like_it'),
    path('logout/', LogoutView.as_view(), name='api_token_delete'),
]

