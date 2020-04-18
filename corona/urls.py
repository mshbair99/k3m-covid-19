from django.urls import path
from . import views

urlpatterns = [

    path('Cases/', views.M_Cases, name='cases'),
    path('about', views.about, name='about'),
    path('covid', views.about_covid, name='aboutCovid'),
    path('blogs', views.blogs, name='blogs'),
    path('Deaths/', views.M_Deaths, name='deaths'),
    path('contact', views.Contact, name='contact'),
    path('blogs/<int:blog_id>/', views.detail, name='detail'),
    path('Recovered/', views.M_Recovered, name='recovered'),
    path('', views.M_Home, name='home'),
]
