from django.urls import path
from accounts import views as accounts_views

app_name = 'accounts'

urlpatterns = [
    path('login/', accounts_views.LoginView.as_view(), name='login'),
    path('logout/', accounts_views.LogoutView.as_view(), name='logout'),
    path('register/', accounts_views.RegisterView.as_view(), name='register'),
    path('<int:user_pk>/', accounts_views.ProfileView.as_view(), name='profile'),
    path('', accounts_views.UserListView.as_view(), name='user_list'),
    # path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    # path('change_password/', ChangePasswordView.as_view(), name='change_password')

]