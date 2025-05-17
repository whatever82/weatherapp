from django.urls import path 

from . import views

app_name = "core"

urlpatterns = [
    path("<str:location>/", views.location, name='location'),
    path("history/<str:latitude>/<str:longitude>/<str:start_date>/<str:end_date>/", views.history, name='history'),
]
