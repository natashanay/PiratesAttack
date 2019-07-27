from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.Pirates),
    url(r'^create_attack/(?P<pirate_id>\d+)$', views.CreateAttack),

]