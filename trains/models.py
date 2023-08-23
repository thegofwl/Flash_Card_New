# Create your models here.

from django.db import models


class Train(models.Model):

    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    train_count = models.IntegerField(default=0)
    update_date = models.DateTimeField(auto_now_add=True)
    # auth.User 는 Django 에 자동 생성 되는 User 테이블
    id_user = models.ForeignKey("auth.User", related_name="train_user", on_delete=models.CASCADE, db_column="id_user")
    id_word = models.ForeignKey("words.Word", related_name="train_word", on_delete=models.CASCADE, db_column="id_word")
