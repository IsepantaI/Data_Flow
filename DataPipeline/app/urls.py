from django.urls import path,include
from . import views
urlpatterns = [
    path('', views.home),
    path('<int:regNo>/',views.AUM_by_regNo),
]
