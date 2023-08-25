from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import LoginForm, RegisterForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
# 회원가입 비밀번호 조건 안맞을 시 표시
from django.contrib.auth.password_validation import validate_password
from django.http import HttpResponse
from django.shortcuts import render, redirect


#회원정보 변경
def profile_edit_view(request):
    if request.method == 'POST':
        user_change_form = UserChangeForm(request.POST, instance=request.user)

        if user_change_form.is_valid():
            if user_change_form.has_changed():
                user_change_form.save()
                messages.success(request, '회원정보가 수정되었습니다.')
            else:
                messages.info(request, '수정 반영되지 않았습니다.')
            return render(request, 'users/profile_edit.html')
        else:
            messages.error(request, '폼 데이터가 유효하지 않습니다. 다시 확인해주세요.')
    else:
        user_change_form = UserChangeForm(instance=request.user)

    return render(request, 'users/profile_edit.html', {'user_change_form': user_change_form})

#비밀번호 변경
@login_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('Information_Modification')
    else:
        password_change_form = PasswordChangeForm(request.user)

    return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})


@login_required
def delete_account(request):
    if request.method == 'POST':
        confirmation = request.POST.get('confirmation')
        withdrawal_button_value = request.POST.get('withdrawal_Button')  # 버튼의 입력값 받아오기
        if confirmation == '회원탈퇴':
            request.user.delete()  # 회원 삭제
            logout(request)  # 로그아웃 처리
        else:
            return HttpResponse(f'탈퇴 요청이 잘못되었습니다. <br>"{withdrawal_button_value}"로 입력함<br>')
    return HttpResponse('삭제되었습니다.')


def sign_in(request):
    if request.method == "GET":
        form = LoginForm()  # LoginForm 인스턴스 생성
        return render(request, 'users/login.html', {'form': form})

    elif request.method == "POST":
        form = LoginForm(request.POST)  # POST 요청 데이터를 사용하여 LoginForm 인스턴스 생성
        if form.is_valid():  # 폼이 유효한지 확인
            username = form.cleaned_data['username']  # 폼에서 사용자명 추출
            password = form.cleaned_data['password']  # 폼에서 비밀번호 추출
            user = authenticate(request, username=username, password=password)  # 사용자 인증 시도
            if user:
                login(request, user)  # 인증된 유저를 로그인시키기 위해 login() 함수 사용
                messages.success(request, f"안녕하세요, {username}님. 환영합니다!")
                return redirect('index')  # 로그인 성공 시 리다이렉트
        messages.error(request, f"유효하지 않은 아이디 또는 비밀번호입니다.")
        return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')  # 로그아웃 후 로그인 페이지로 리디렉션


def register(request):
    if request.method == "GET":
        form = RegisterForm()  # RegisterForm 인스턴스 생성
        return render(request, 'users/register.html', {'form': form})

    elif request.method == "POST":
        form = RegisterForm(request.POST)  # POST 요청 데이터를 사용하여 RegisterForm 인스턴스 생성
        if form.is_valid():  # 폼이 유효한지 확인
            user = form.save(commit=False)  # 폼을 기반으로 User 모델 인스턴스 생성 (아직 저장하지 않음)
            user.username = user.username.lower()  # 사용자명을 소문자로 변환하여 저장
            # 비밀번호 검증 추가
            password = form.cleaned_data.get('password1')
            try:
                validate_password(password, user=user)
            except ValidationError as error:
                form.add_error('password1', error)
                return render(request, 'users/register.html', {'form': form})
            user.set_password(password)
            #
            user.save()  # 사용자 정보 저장
            messages.success(request, f"Signup Success")
            return redirect('login')  # 회원가입 성공 시 로그인 페이지로 리다이렉트
        messages.error(request, f"Signup 실패")
        return render(request, 'users/register.html', {'form': form})


def search_id(request):
    id_found = False  # 아이디를 찾았는지 여부를 나타내는 변수 초기화
    found_id = ""  # 찾은 아이디를 저장하는 변수 초기화
    if request.method == "POST":  # POST 요청인 경우에만 처리
        first_name = request.POST.get('first_name')  # POST 데이터에서 이름 추출
        last_name = request.POST.get('last_name')  # POST 데이터에서 성 추출
        try:
            user = User.objects.get(first_name=first_name, last_name=last_name)  # 이름과 성으로 사용자 검색
            id_found = True  # 아이디를 찾았음을 표시
            found_id = user.username  # 찾은 사용자의 아이디 저장
            messages.success(request, f"{first_name + last_name}님의 아이디를 찾았습니다.")  # 성공 메시지 추가
        except User.DoesNotExist:  # 해당 조건의 사용자가 없는 경우
            messages.error(request, f"입력한 이름과 성에 해당하는 사용자가 없습니다.")  # 에러 메시지 추가
    return render(request, 'users/search_id.html', {'id_found': id_found, 'found_id': found_id})


# 사용자 검증과 비밀번호 재설정 함수
def check_user_and_reset_password(request, user, new_password):
    form = SetPasswordForm(user, {'new_password1': new_password, 'new_password2': new_password})
    if form.is_valid():
        form.save()
        logout(request)
        user = authenticate(request, username=user.username, password=new_password)
        if user:
            login(request, user)
            messages.success(request, f"비밀번호가 성공적으로 변경되었습니다. 다시 로그인해주세요.")
            return redirect('login')
        else:
            messages.error(request, f"비밀번호 변경 후 로그인 중 오류가 발생했습니다.")
            return redirect('login')
    else:
        messages.error(request, f"비밀번호 변경 중 오류가 발생했습니다.")
        return redirect('find_password')


# 사용자 검증 함수
def check_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            return render(request, 'users/find_password.html', {'password_found': True, 'user': user})
        except User.DoesNotExist:
            messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다.")
    return render(request, 'users/find_password.html', {'password_found': False})


# 비밀번호 재설정 뷰
def find_password(request):
    if request.method == "POST" and request.POST.get('new_password'):
        username = request.POST.get('username')
        email = request.POST.get('email')
        try:
            user = User.objects.get(username=username, email=email)
            new_password = request.POST.get('new_password')
            return check_user_and_reset_password(request, user, new_password)
        except User.DoesNotExist:
            messages.error(request, f"해당 이름 또는 이메일로 된 사용자가 없습니다.")
    elif request.method == "POST":
        return check_user(request)
    return render(request, 'users/find_password.html', {'password_found': False})


def index(request):
    return render(request, 'users/index.html')


def Information_Modification(request):
    return render(request, 'users/Information_Modification.html')


def Withdrawal(request):
    return render(request, 'users/Withdrawal.html')

def profile_edit(request):
    return render(request, 'users/profile_edit.html')

