from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db import connection
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from words.crawling.daum_dict import DaumDict
from words.models import Word


# Create your views here.
class WordList(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        words = Word.objects.all().order_by('-id')
        paginator = Paginator(words, 15)
        page_number = request.GET.get("page")
        word_list = paginator.get_page(page_number)
        context = {'word_list': word_list}
        return render(request, 'words/word_list.html', context)

    def post(self, request):
        word_id = request.POST.get('word_id')
        try:
            word = Word.objects.get(id=word_id)
            word.delete()
            message = "단어가 삭제되었습니다."
        except Word.DoesNotExist:
            message = "삭제할 단어를 찾을 수 없습니다."

        return WordUtil.get_system_message_render(request, message, 'words')


class WordInput(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        return render(request, 'words/word_input.html')

    def post(self, request):
        input_word: str = request.POST.get('input_word')
        if input_word is None or input_word.strip() == "":
            error_message = "단어를 입력하세요."
            return WordUtil.get_system_message_render(request, error_message, 'word-input')

        input_word_list = WordUtil.get_word_list(input_word)
        find_word_list_dict = WordUtil.find_reg_word(input_word_list)
        input_word_list = find_word_list_dict['input_word_list']
        find_message = find_word_list_dict['find_message']

        if len(input_word_list) > 0:
            find_word_dict = WordUtil.get_daum_dict(input_word_list[0])
            show_word_list = WordUtil.get_show_word_list(find_word_dict['is_success'], input_word_list, 0)
            context = {'show_word_list': show_word_list, 'input_word_list': input_word_list,
                       'find_message': find_message,
                       'find_word_num': 0, 'find_word_dict': find_word_dict}
            return render(request, 'words/word_find.html', context)

        else:
            return WordUtil.get_system_message_render(request, find_message, 'word-input')


class WordSave(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request):
        return WordUtil.get_system_message_render(request, "페이지 접근 오류 ", 'word-input')

    def post(self, request):
        word = WordUtil.get_word(request)
        word.save()
        input_word_list = request.POST.getlist('input_word_list')
        find_word_num = int(request.POST['find_word_num'])
        find_message = request.POST['find_message']

        if find_word_num < len(input_word_list) - 1:
            find_word_num += 1
            find_word_dict = WordUtil.get_daum_dict(input_word_list[find_word_num])
            show_word_list = WordUtil.get_show_word_list(find_word_dict['is_success'], input_word_list, find_word_num)
            context = {'show_word_list': show_word_list, 'input_word_list': input_word_list,
                       'find_message': find_message, 'find_word_num': find_word_num, 'find_word_dict': find_word_dict}
            return render(request, 'words/word_find.html', context)
        else:
            return redirect('words')


class WordEdit(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정

    def get(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)
        context = {'word': word}
        return render(request, 'words/word_edit.html', context)

    def post(self, request, word_id):
        word = get_object_or_404(Word, id=word_id)

        en_word = request.POST.get('en_word')
        en_phonetic = request.POST.get('en_phonetic')
        word_class = request.POST.get('word_class')
        ko_phonetic = request.POST.get('ko_phonetic')
        ko_word_1 = request.POST.get('ko_word_1')
        ko_word_2 = request.POST.get('ko_word_2')
        ko_romanize = request.POST.get('ko_romanize')

        # 단어 정보 업데이트
        word.en_word = en_word
        word.en_phonetic = en_phonetic
        word.word_class = word_class
        word.ko_phonetic = ko_phonetic
        word.ko_word_1 = ko_word_1
        word.ko_word_2 = ko_word_2
        word.ko_romanize = ko_romanize
        word.save()

        return redirect('words')


class WordClear(LoginRequiredMixin, View):
    login_url = 'login'  # 로그인 페이지 URL 설정


    def get(self, request):
        return render(request, 'words/word_clear.html')

    def post(self, request):
        clear_password = 'qwer1234'
        get_password = request.POST.get('clear_password')
        if clear_password == get_password:
            Word.objects.all().delete()
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'words_word'")
            return redirect('words')  # Redirect to the desired URL
        else:
            return WordUtil.get_system_message_render(request, "비밀번호 오류 ", 'words')


class WordUtil:
    @staticmethod
    def get_word_list(input_word):
        input_word = input_word.replace(" ", "").replace("\r", "").replace("\n", "")
        input_word_list = input_word.split(',')
        if input_word_list[len(input_word_list) - 1] == "":
            input_word_list.pop(len(input_word_list) - 1)
        return input_word_list

    @staticmethod
    def find_reg_word(input_word_list: list):
        find_word_list = list(input_word_list)
        find_words = []
        for word in input_word_list:
            try:
                select_word = Word.objects.get(en_word=word)
                print(select_word)
                find_words.append(word)
                find_word_list.remove(word)
            except ObjectDoesNotExist:
                print(f"No data found with en_word {word}")

        if len(find_words) == 0:
            find_message = "모든 단어 등록 가능합니다."
        elif len(find_words) == len(input_word_list):
            find_message = "이미 등록된 단어입니다."
        else:
            find_message = f"이미 등록된 단어: [{', '.join(find_words)}]"
        print(find_message)
        return {'input_word_list': find_word_list, 'find_message': find_message}

    @staticmethod
    def get_daum_dict(input_word):
        daum_dict = DaumDict(input_word)
        daum_dict.is_get_detail_page()
        find_word_dict = daum_dict.get_word_dict()
        return find_word_dict

    @staticmethod
    def get_show_word_list(is_success: bool, input_word_list, bold_num):
        show_word_list = ''
        if is_success:
            for index, word in enumerate(input_word_list):
                if index == bold_num:
                    show_word_list += f'<b>[{word}]</b>'
                    if index < len(input_word_list) - 1:
                        show_word_list += ", "
                elif index < len(input_word_list) - 1:
                    show_word_list += f'{word}, '
                else:
                    show_word_list += f'{word}'
        else:
            show_word_list = '검색 실패'
        return show_word_list

    @staticmethod
    def get_word(request):
        word_data = {
            'en_word': request.POST['en_word'],
            'en_phonetic': request.POST['en_phonetic'],
            'word_class': request.POST['word_class'],
            'ko_phonetic': request.POST['ko_phonetic'],
            'ko_word_1': request.POST['ko_word_1'],
            'ko_word_2': request.POST['ko_word_2'],
            'ko_romanize': request.POST['ko_romanize'],
        }
        word = Word(**word_data)
        return word

    @staticmethod
    def get_system_message_render(request, error_message, set_urls):
        context = {'system_message': error_message, 'set_urls': set_urls}
        return render(request, 'system_message.html', context)


"""
every,
example,
excellent,
excite,
excuse,
exercise,
eye,
face,
fact,
fair,
fall
"""
