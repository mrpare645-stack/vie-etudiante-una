from django.urls import path
from . import views

app_name = 'vie_estudiantine_una'

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('actualites/', views.courses, name='courses'),
    path('course-details/<int:id>/', views.course_details, name='course_details'),
    path('events/', views.events, name='events'),
    path('crouA2/', views.pricing, name='pricing'),
    path('club/', views.trainers, name='trainers'),
]
