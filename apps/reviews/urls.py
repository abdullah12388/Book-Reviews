from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
    url(r'^books/?$', views.showBooks),
    url(r'^books/add/?$', views.addBook),
    url(r'^books/(?P<number>\d+)/?$', views.showOneBook),
    url(r'^users/(?P<number>\d+)/?$', views.showUser),
    url(r'^process_login/?$', views.processLogin),
    url(r'^process_registration/?$', views.processRegistration),
    url(r'^logout/?$', views.logout),
