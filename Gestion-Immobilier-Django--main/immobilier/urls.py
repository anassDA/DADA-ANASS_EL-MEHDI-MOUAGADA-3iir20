from django.urls import path
from . import views
from django.contrib.auth import views as auth_views






urlpatterns = [
    path('', views.immobilier_list, name='immobilier_list'),
    path('<int:pk>/', views.immobilier_detail, name='immobilier_detail'),
    path('new/', views.immobilier_create, name='immobilier_create'),
    path('<int:pk>/edit/', views.immobilier_update, name='immobilier_update'),
    path('<int:pk>/delete/', views.immobilier_delete, name='immobilier_delete'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path('account/logout-confirm/', views.logout_confirm, name='logout_confirm'),
    path('account/logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup')
]
