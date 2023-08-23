from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views import View

from users.models import Config




class ExamsSetting(LoginRequiredMixin, View):
    #      LoginRequiredMixin 로그인 되어 있는지 확인하고 안되어 있으면 러그린 화면으로 가는 class
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        user = request.user
        try:
            config = Config.objects.get(id_user=user.id)
        except ObjectDoesNotExist:
            config = Config()
        context = {'config': config}
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
        print(config_data_dict)
        try:
            config = Config.objects.get(id_user=user.id)
            ExamUtil.config_save(config, config_data_dict)
        except ObjectDoesNotExist:
            config = Config()
            config.id_user = user
            ExamUtil.config_save(config, config_data_dict)

        return render(request, 'exams/exams_start.html')


class ExamUtil:
    @staticmethod
    def config_save(config: Config, config_data_dict):
        config.exam_word_count = config_data_dict['exam_word_count']
        config.exam_seconds = config_data_dict['exam_seconds']
        config.exam_tts_play = config_data_dict['exam_tts_play']
        config.exam_difficulty = config_data_dict['exam_difficulty']
        config.save()



def Information_Modification(request):
    return render(request, 'exams/Information_Modification.html')


def Withdrawal(request):
    return render(request, 'exams/Withdrawal.html')

def Word_Test_History(request):
    return render(request, 'exams/Word_Test_History.html')


def Word_Test_Score(request):
    return render(request, 'exams/Word_Test_Score.html')

