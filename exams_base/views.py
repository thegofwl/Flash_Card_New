import random

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.forms import model_to_dict
from django.shortcuts import render
from django.views import View

from users.models import Config
from words.models import Word




class ExamsSetting(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        user = request.user
        try:
            config = Config.objects.get(id_user=user.id)
        except ObjectDoesNotExist:
            config = Config()
        context = {'config': config}
        return render(request, 'exams_base/exam_base_setting.html', context)

    def post(self, request):
        user = request.user

        exam_word_count = request.POST.get('exam_word_count')
        exam_seconds = request.POST.get('exam_seconds')
        exam_tts_play = request.POST.get('exam_tts_play')
        exam_types = request.POST.get('exam_types')
        hint_type = request.POST.get('hint_type')
        config_data_dict = {
            'exam_word_count': exam_word_count,
            'exam_seconds': exam_seconds,
            'exam_tts_play': exam_tts_play,
        }
        temp_data_dict = {
            'exam_types': exam_types,
            'hint_type': hint_type,
        }
        print(config_data_dict)
        print(temp_data_dict)
        try:
            config = Config.objects.get(id_user=user.id)
            ExamUtil.config_save(config, config_data_dict)
        except ObjectDoesNotExist:
            config = Config()
            config.id_user = user
            ExamUtil.config_save(config, config_data_dict)

        exam_count = int(exam_word_count)
        ExamUtil.exam_type = exam_types
        ExamUtil.exam_seconds = int(exam_seconds)
        if hint_type:
            ExamUtil.hint_type = int(hint_type)

        all_words = Word.objects.all()
        ExamUtil.exam_word_list = random.sample(list(all_words), exam_count)
        exam_word_dict = ExamUtil.get_exam_word_dict(ExamUtil.exam_word_list[0])
        exam_word_with_opt = ExamUtil.set_exam_word_options(exam_word_dict)
        context = {'exam_word': exam_word_with_opt, 'show_num': 1}
        return render(request, 'exams_base/exam_base_show.html', context)


class ExamsShow(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        pass

    def post(self, request):
        show_num = int(request.POST.get('show_num'))

        if show_num < len(ExamUtil.exam_word_list):
            exam_word_dict = ExamUtil.get_exam_word_dict(ExamUtil.exam_word_list[show_num])
            print(exam_word_dict)
            exam_word_with_opt = ExamUtil.set_exam_word_options(exam_word_dict)
            context = {'exam_word': exam_word_with_opt, 'show_num': show_num + 1}
            return render(request, 'exams_base/exam_base_show.html', context)
        else:
            return ExamUtil.get_system_message_render(request, "TEST 통계 페이지 구현 하기 ", 'exam_base-setting')


class ExamUtil:
    exam_type = 'en'
    hint_type = 0
    exam_seconds = 0
    exam_word_list = []

    @staticmethod
    def config_save(config: Config, config_data_dict):
        config.exam_word_count = config_data_dict['exam_word_count']
        config.exam_seconds = config_data_dict['exam_seconds']
        config.exam_tts_play = config_data_dict['exam_tts_play']
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
    def set_exam_word_options(exam_word_dict):
        exam_word_dict['exam_seconds'] = ExamUtil.exam_seconds * 1000
        exam_word_dict['exam_redirect_seconds'] = exam_word_dict['exam_seconds'] + 500

        exam_word_dict['exam_types'] = ExamUtil.exam_type

        if exam_word_dict['exam_types'] == 'en':
            exam_word_dict['exam_question'] = exam_word_dict['ko_word_1']
            exam_word_dict['exam_hint'] = exam_word_dict['en_word']
            exam_word_dict['hint_type'] = ExamUtil.hint_type

            if exam_word_dict['hint_type'] == 1:
                exam_word_dict['exam_hint'] = len(exam_word_dict['exam_hint'])
            elif exam_word_dict['hint_type'] == 2:
                exam_word_dict['exam_hint'] = ExamUtil.get_conceal_en_word(exam_word_dict['exam_hint'])
        else:
            exam_word_dict['exam_question'] = exam_word_dict['en_word']


        return exam_word_dict

    @staticmethod
    def get_conceal_en_word(en_word):
        letter_list = list(en_word)
        word_length = len(en_word)
        for i in random.sample(range(word_length), (word_length + 1) // 2):
            letter_list[i] = ' _ '
        return ''.join(letter_list)

    @staticmethod
    def get_system_message_render(request, error_message, set_urls):
        context = {'system_message': error_message, 'set_urls': set_urls}
        return render(request, 'system_message.html', context)
