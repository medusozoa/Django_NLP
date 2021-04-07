from django.urls import path
from . import views

app_name= "QandA"
urlpatterns = [
    path("", views.index, name="index"),
    path("addQuestion", views.addQuestion, name="addQuestion"),
    path("addText", views.addText, name="addText")
]