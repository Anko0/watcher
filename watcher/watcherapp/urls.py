from rest_framework.urlpatterns import format_suffix_patterns

from django.urls import path

from . import views


urlpatterns = [
    path('', views.Index.as_view()),
    path('add/active/', views.AddActive.as_view(), name='add_active'),
    path('edit/active/<int:pk>/', views.EditActive.as_view(), name='edit_active'),
    path('delete/active/<int:pk>/', views.DeleteActive.as_view(), name='delete_active'),
    path('show/actives/', views.ShowActives.as_view(), name='show_actives'),
    path('show/active/<int:pk>/', views.ShowActive.as_view(), name='show_active'),
    path('active/', views.ActiveList.as_view()),
    path('active/<int:pk>/', views.ActiveDetail.as_view()),
    path('metrix/', views.MetrixList.as_view()),
    path('metrix/<int:pk>/', views.MetrixDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
