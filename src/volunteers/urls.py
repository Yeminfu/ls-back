# ./volunteers/urls.py

from django.urls import path

from .views import VolunteerListView, VolunteerCreateView

urlpatterns = [
    path(
        "volunteers/",
        VolunteerListView.as_view(),
        name="volunteer-list",
    ),
    path(
        "volunteers/create/",
        VolunteerCreateView.as_view(),
        name="volunteer-create",
    ),
]