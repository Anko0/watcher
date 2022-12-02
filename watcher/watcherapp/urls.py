from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from . import views


urlpatterns = [
    path('', views.Index.as_view()),
    path('add/email/', views.AddEmail.as_view(), name='add_email'),
    path('delete/email/<int:pk>/', views.DeleteEmail.as_view(), name='delete_email'),
    path('show/emails/', views.ShowEmails.as_view(), name='show_emails'),
    path('add/active/', views.AddActive.as_view(), name='add_active'),
    path('edit/active/<int:pk>/', views.EditActive.as_view(), name='edit_active'),
    path('delete/active/<int:pk>/', views.DeleteActive.as_view(), name='delete_active'),
    path('show/actives/', views.ShowActives.as_view(), name='show_actives'),
    path('show/active/<int:pk>/', views.ShowActive.as_view(), name='show_active'),
    path('metrix/', views.MetrixList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)