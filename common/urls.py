from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('roster/', views.RosterView.as_view(), name='roster'),
]