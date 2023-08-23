from django.urls import path

from words import views

urlpatterns = [
    path("", views.WordList.as_view(), name="words"),
    path("word-input/", views.WordInput.as_view(), name="word-input"),
    path("word-save/", views.WordSave.as_view(), name="word-save"),
    path("word/<int:word_id>/", views.WordEdit.as_view(), name="word-edit"),
    path("word-clear/", views.WordClear.as_view(), name="word-clear"),
    path("word-reset/", views.WordReset.as_view(), name="word-reset"),
]
