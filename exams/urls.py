from django.urls import path

from exams import views

urlpatterns = [
    path("Word_Test_History/", views.Word_Test_History, name="Word_Test_History"),
    path("Word_Test_Score/", views.Word_Test_Score, name="Word_Test_Score"),

    # 용석 작업 - 기존 작업 유지 하고 추가 작업 합니다. - 나중에 확인 하세요.
    path("exam-setting/", views.ExamsSetting.as_view(), name="exam-setting"),

]
