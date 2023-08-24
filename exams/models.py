from django.db import models


class Exam(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    exam_type = models.CharField(max_length=10, default='en')  # 문제타입 - en = 한글뜻 보이고 영어 맞추기, ko = 영어 보이고 한글 맞추기
    in_word = models.CharField(max_length=50)
    exam_right = models.BooleanField()
    exam_point = models.FloatField()
    exam_difficulty = models.IntegerField(default=1)
    reg_date = models.DateTimeField(auto_now_add=True)
    # auth.User 는 Django 에 자동 생성 되는 User 테이블
    id_user = models.ForeignKey("auth.User", related_name="exam_user", on_delete=models.CASCADE, db_column="id_user")
    id_word = models.ForeignKey("words.Word", related_name="word", on_delete=models.CASCADE, db_column="id_word")
