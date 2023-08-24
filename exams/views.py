import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import render
from django.views import View

from exams.models import Exam
from users.models import Config
from words.models import Word


class ExamsSetting(LoginRequiredMixin, View):
    #      LoginRequiredMixin 로그인 되어 있는지 확인하고 안되어 있으면 러그린 화면으로 가는 class
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        user = request.user
        try:
            config = Config.objects.get(id_user=user.id)
        except ObjectDoesNotExist:
            config = Config()
        context = {'config': config, 'levels': ExamUtil.levels}
        return render(request, 'exams/exams_setting.html', context)

    def post(self, request):
        user = request.user

        exam_word_count = request.POST.get('exam_word_count')
        exam_seconds = request.POST.get('exam_seconds')
        exam_tts_play = request.POST.get('exam_tts_play')
        exam_difficulty = request.POST.get('exam_difficulty')
        config_data_dict = {
            'exam_word_count': exam_word_count,
            'exam_seconds': exam_seconds,
            'exam_tts_play': exam_tts_play,
            'exam_difficulty': exam_difficulty,
        }
        try:
            config = Config.objects.get(id_user=user.id)
            ExamUtil.config_save(config, config_data_dict)
        except ObjectDoesNotExist:
            config = Config()
            config.id_user = user
            ExamUtil.config_save(config, config_data_dict)

        exam_count = int(exam_word_count)
        ExamUtil.exam_difficulty = int(exam_difficulty)
        all_words = Word.objects.all()
        ExamUtil.exam_word_list = random.sample(list(all_words), exam_count)  # 중복 없는 랜덤 Word 리스트 생성
        exam_word_dict = ExamUtil.get_exam_word_dict(ExamUtil.exam_word_list[0])
        ExamUtil.exam_word_difficulty = ExamUtil.set_exam_word_difficulty(exam_word_dict)
        context = {'exam_word': ExamUtil.exam_word_difficulty, 'show_num': 1}
        return render(request, 'exams/exams_show.html', context)


class ExamsShow(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        pass

    def post(self, request):
        show_num = int(request.POST.get('show_num'))
        word_user_input = request.POST.get('word_user_input')
        user = request.user

        en_word = ExamUtil.exam_word_difficulty['en_word']
        ko_word_1 = ExamUtil.exam_word_difficulty['ko_word_1']

        exam = Exam()
        exam.in_word = word_user_input
        exam.exam_type = ExamUtil.exam_word_difficulty['exam_types']
        exam.exam_right, exam.exam_point = ExamUtil.get_exam_right(exam.exam_type, exam.in_word, en_word, ko_word_1)
        exam.id_word = ExamUtil.exam_word_list[show_num - 1]
        exam.id_user = user
        exam.save()

        if show_num < len(ExamUtil.exam_word_list):
            exam_word_dict = ExamUtil.get_exam_word_dict(ExamUtil.exam_word_list[show_num])
            ExamUtil.exam_word_difficulty = ExamUtil.set_exam_word_difficulty(exam_word_dict)
            context = {'exam_word': ExamUtil.exam_word_difficulty, 'show_num': show_num + 1}
            return render(request, 'exams/exams_show.html', context)
        else:
            return ExamUtil.get_system_message_render(request, "TEST 통계 페이지 구현 하기 ", 'exam-setting')


class ExamUtil:
    levels = range(1, 6)

    exam_difficulty = 1
    exam_word_list = []

    exam_word_difficulty = {}

    @staticmethod
    def config_save(config: Config, config_data_dict):
        config.exam_word_count = config_data_dict['exam_word_count']
        config.exam_seconds = config_data_dict['exam_seconds']
        config.exam_tts_play = config_data_dict['exam_tts_play']
        config.exam_difficulty = config_data_dict['exam_difficulty']
        config.save()

    @staticmethod
    def get_en_phonetics(en_phonetics):
        if ',' in en_phonetics:
            phonetics = en_phonetics.strip().split(',')
            make_phonetics = f"미국식:[{phonetics[0]}],  영국식:[{phonetics[1]}]"
        else:
            make_phonetics = f"미국식:[{en_phonetics}],  영국식:[{en_phonetics}]"
        return make_phonetics

    @staticmethod
    def get_exam_word_dict(exam_word):
        exam_word_dict = model_to_dict(exam_word)
        exam_word_dict['en_phonetic'] = ExamUtil.get_en_phonetics(exam_word_dict['en_phonetic'])
        exam_word_dict['word_class'] = f"{{{exam_word_dict['word_class']}}}"
        exam_word_dict['ko_phonetic'] = f"({exam_word_dict['ko_phonetic']})"
        exam_word_dict['ko_romanize'] = f"[{exam_word_dict['ko_romanize']}]"

        if ',' in exam_word_dict['ko_word_2']:
            exam_word_dict['ko_word_2'] = exam_word_dict['ko_word_2'].replace(',', ', ')
        return exam_word_dict

    @staticmethod
    def set_exam_word_difficulty(exam_word_dict):
        show_time = 6
        # 당어가 보여지는 타임 설정
        exam_word_dict['exam_seconds'] = ((show_time - ExamUtil.exam_difficulty) * 2) * 1000
        exam_word_dict['exam_redirect_seconds'] = exam_word_dict['exam_seconds'] + 500
        exam_word_dict['exam_difficulty'] = ExamUtil.exam_difficulty

        # 레벨에 맞춰 보여지는 타입 설정
        exam_word_dict['exam_types'] = ExamUtil.get_exam_types(ExamUtil.exam_difficulty)

        # 타입에 맞춰 문제 단어 저장
        if exam_word_dict['exam_types'] == 'en':
            exam_word_dict['exam_question'] = exam_word_dict['ko_word_1']
            exam_word_dict['exam_placeholder'] = "영어 단어를 입력하세요"
        else:
            exam_word_dict['exam_question'] = exam_word_dict['en_word']
            exam_word_dict['exam_placeholder'] = "한글 뜻을 입력하세요"

            # 1 레벨은 영어 단어중 몇개의 스페링 가림
        if ExamUtil.exam_difficulty == 1:
            exam_word_dict['exam_question'] = exam_word_dict['en_word']
            exam_word_dict['exam_question'] = ExamUtil.get_conceal_en_word(exam_word_dict['exam_question'])
            exam_word_dict['exam_placeholder'] = "영어 단어를 완성 하세요"

        return exam_word_dict

    @staticmethod
    def get_exam_types(level):
        exam_types = ['en', 'ko']  # en = 한글뜻 보이고 영어 맞추기, ko = 영어 보이고 한글 맞추기
        if level in [1, 3]:
            exam_type = exam_types[0]
        elif level == 2:
            exam_type = exam_types[1]
        else:
            exam_type = random.choice(exam_types)

        return exam_type

    @staticmethod
    def get_conceal_en_word(en_word):  # 장우림님 제작 메소드
        letter_list = list(en_word)
        word_length = len(en_word)
        num_concealed = random.randrange(word_length // 3, word_length // 2 + 1)
        for i in random.sample(range(word_length), num_concealed):
            letter_list[i] = '_ '
        return ''.join(letter_list)

    @staticmethod
    def get_exam_right(exam_type, in_word, en_word, ko_word_1):
        exam_point = 100.00

        if exam_type == 'en':
            exam_right = (en_word == in_word)
        else:
            exam_right = (ko_word_1 == in_word)

        if not exam_right:
            exam_point = ExamUtil.get_exam_point(in_word, en_word) if exam_type == 'en' else 0.0

        return exam_right, exam_point

    @staticmethod
    def get_exam_point(input_word, correct_word):
        # 정답과 입력된 단어를 소문자로 변환하여 비교
        input_word = input_word.lower()
        correct_word = correct_word.lower()

        # 문자 하나씩 비교하여 정확도 계산
        correct_chars = sum(1 for a, b in zip(input_word, correct_word) if a == b)
        accuracy = round((correct_chars / len(correct_word)) * 100, 2)

        return accuracy

    @staticmethod
    def get_system_message_render(request, error_message, set_urls):
        context = {'system_message': error_message, 'set_urls': set_urls}
        return render(request, 'system_message.html', context)


def home(request):
    return render(request, 'exams/home.html')


def Information_Modification(request):
    return render(request, 'exams/Information_Modification.html')


def Withdrawal(request):
    return render(request, 'exams/Withdrawal.html')


def Word_Practice(request):
    return render(request, 'exams/Word_Practice.html')


def Word_Practice_Set(request):
    return render(request, 'exams/Word_Practice_Set.html')


def Word_Test(request):
    return render(request, 'exams/Word_Test.html')


def Word_Test_History(request):
    return render(request, 'exams/Word_Test_History.html')


def Word_Test_Score(request):
    return render(request, 'exams/Word_Test_Score.html')


def Word_Test_Set(request):
    return render(request, 'exams/Word_Test_Set.html')
