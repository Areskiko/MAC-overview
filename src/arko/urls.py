from django.urls import path
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.Home, name="Arko-home"),
    path('scanner', views.Scanner, name="Arko-scanner"),
    path('tracked', views.Tracked, name="Arko-tracked"),
    path('untracked', views.Untracked, name="Arko-untracked"),
    path('removeTracked', views.RemoveTrack, name="Arko-removeTracked"),
]