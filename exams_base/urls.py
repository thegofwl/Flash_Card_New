from django.urls import path

from exams_base import views

urlpatterns = [
    path("exam_base-setting/", views.ExamsSetting.as_view(), name="exam_base-setting"),
    path("exam_base-show/", views.ExamsShow.as_view(), name="exam_base-show"),
]
