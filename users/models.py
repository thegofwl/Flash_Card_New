from django.db import models


# Create your models here.

class Config(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    train_word_count = models.IntegerField(default=0)
    train_seconds = models.IntegerField(default=0)
    train_repeat = models.IntegerField(default=0)
    train_tts_play = models.BooleanField(default=False)
    exam_word_count = models.IntegerField(default=0)
    exam_seconds = models.IntegerField(default=0)
    exam_tts_play = models.BooleanField(default=False)
    exam_difficulty = models.IntegerField(default=0)
    user_find_hint = models.CharField(max_length=100, default='Korea')
    update_date = models.DateTimeField(auto_now_add=True)
    # auth.User 는 Django 에 자동 생성 되는 User 테이블
    id_user = models.ForeignKey("auth.User", related_name="config_user", on_delete=models.CASCADE, db_column="id_user")
