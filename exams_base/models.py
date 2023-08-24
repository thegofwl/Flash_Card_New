from django.db import models


class Exam_base(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)
    in_word = models.CharField(max_length=50)
    exam_right = models.BooleanField()
    exam_point = models.DecimalField(max_digits=3, decimal_places=2)
    reg_date = models.DateTimeField(auto_now_add=True)
    # auth.User 는 Django 에 자동 생성 되는 User 테이블
    id_user = models.ForeignKey("auth.User", related_name="exam_base_user", on_delete=models.CASCADE, db_column="id_user")
    id_word = models.ForeignKey("words.Word", related_name="exam_base_word", on_delete=models.CASCADE, db_column="id_word")
