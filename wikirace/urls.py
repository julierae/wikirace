from django.urls import path
from wikirace import views

urlpatterns = [
    path("", views.input_view, name="input"),
    path("results/", views.results_view, name="results"),
]
