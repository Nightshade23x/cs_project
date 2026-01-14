from django.urls import path
from . import views

urlpatterns = [
    path("note/<int:note_id>/", views.view_note, name="view_note"),
]
