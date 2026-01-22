from django.urls import path
from . import views

urlpatterns = [
    path("note/<int:note_id>/", views.view_note, name="view_note"),
    path("search/", views.search_notes, name="search_notes"),
    path("insecure-login/", views.insecure_login, name="login"),
    path("login/", views.insecure_login, name="login"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),
]
