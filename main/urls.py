from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^login$', views.login_user, name='login'),
    url(r'^home$', views.home, name='home'),
    url(r'^logout$', views.log_out, name='logout')
]