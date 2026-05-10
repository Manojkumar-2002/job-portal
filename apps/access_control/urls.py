from .views import SetPersonaView
from django.urls import path


urlpatterns = [
    path("set-persona/", SetPersonaView.as_view(), name="set-persona"),
]