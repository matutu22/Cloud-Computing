from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^se\d_show',views.senarios_show, name = 'senarios_show'),
    url(r'^se', views.senarios, name = 'senarios'),
    url(r'^.+', views.index, name='index'),
]
