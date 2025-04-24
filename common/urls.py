from django.urls import path
from . import views

app_name = 'common'

urlpatterns = [
    path('roster/', views.RosterView.as_view(), name='roster'),
    path('programs/', views.ProgramListApiView.as_view(), name='programs-list'),
    path('university/<int:pk>/', views.UniversityRetrieveApiView.as_view(), name='university-detail'),
]