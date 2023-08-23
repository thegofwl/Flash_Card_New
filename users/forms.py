from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# 사용자 로그인 폼 정의
class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)  # 아이디 입력 필드
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)  # 비밀번호 입력 필드

# 사용자 회원가입 폼 정의
class RegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, label='이름')  # 이름 입력 필드
    last_name = forms.CharField(max_length=30, label='성')   # 성 입력 필드
    class Meta:
        model = User  # 내장 User 모델을 사용
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        # 폼에서 사용할 필드들을 지정


