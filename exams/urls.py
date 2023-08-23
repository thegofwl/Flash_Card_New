from django.urls import path

from exams import views

urlpatterns = [
    path("home/", views.home, name="home"),
    path("Information_Modification/", views.Information_Modification, name="Information_Modification"),
    path("Withdrawal/", views.Withdrawal, name="Withdrawal"),
    path("Word_Test_History/", views.Word_Test_History, name="Word_Test_History"),
    path("Word_Test_Score/", views.Word_Test_Score, name="Word_Test_Score"),
    path('delete_account/', views.delete_account, name='delete_account'),

    # 용석 작업 - 기존 작업 유지 하고 추가 작업 합니다. - 나중에 확인 하세요.
    path("exam-setting/", views.ExamsSetting.as_view(), name="exam-setting"),

]
