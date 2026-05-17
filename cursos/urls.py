from django.urls import path

from . import views

app_name = "cursos"

urlpatterns = [
    path("", views.lista_cursos, name="lista"),
    path("cursos/<slug:slug>/", views.detalhe_curso, name="detalhe"),
]
