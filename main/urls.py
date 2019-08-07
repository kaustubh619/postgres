from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    # url(r'^login$', views.login_user, name='login'),
    url(r'^$', views.home, name='home'),
    url(r'^logout$', views.log_out, name='logout'),
    url(r'^register$', views.sign_up, name='register'),
    path('activate/<uid>/<token>', views.activate, name="activate")
]