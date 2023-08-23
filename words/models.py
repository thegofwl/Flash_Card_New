from django.db import models


class Word(models.Model):
    # id = models.IntegerField(primary_key=True, auto_created=True)  -> id 는 자동 생성됨
    en_word = models.CharField(max_length=30)
    en_phonetic = models.CharField(max_length=30)
    word_class = models.CharField(max_length=30)
    ko_phonetic = models.CharField(max_length=30)
    ko_word_1 = models.CharField(max_length=50)
    ko_word_2 = models.CharField(max_length=50)
    ko_romanize = models.CharField(max_length=50)
    reg_date = models.DateTimeField(auto_now_add=True)
