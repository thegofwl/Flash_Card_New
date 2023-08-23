import requests
from bs4 import BeautifulSoup


class DaumDict:

    # https://dic.daum.net/search.do?q=zoo&dic=eng
    # https://dic.daum.net/word/view.do?wordid=ekw000189695

    def __init__(self, word) -> None:
        self.daum_dic = "https://dic.daum.net"
        self.__word = word
        self.__inner_top = None
        self.__card_sort = None
        self.__is_get_detail_page = False
        self.__none_str = "자료 없음"
        self.__join_str = ","

    # 다음 사전 상세 페이지 크롤링
    def is_get_detail_page(self):
        try:
            # 다음 사전 검색 페이지 크롤링
            daum_dic_url = f"{self.daum_dic}/search.do?q={self.__word}"
            resp = requests.get(daum_dic_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            daum_dic_detail = soup.select_one('a.txt_cleansch').attrs['href']
            detail_url = self.daum_dic + daum_dic_detail

            # 다음 사전 상세 페이지 크롤링
            resp = requests.get(detail_url)
            soup = BeautifulSoup(resp.text, 'html.parser')

            # 상단 영어단어, 단어뜻, 발음기호 추출
            self.__inner_top = soup.find('div', class_='inner_top')
            self.__card_sort = soup.find('div', class_='wrap_sort')
            self.__is_get_detail_page = True
        except Exception as e:
            print(repr(e))

        return self.__is_get_detail_page

    def __get_ko_word_1(self, inner_top):
        ko_word_1 = self.__none_str
        try:
            ko_word_list = inner_top.find("ul", class_='list_mean')
            span_mean_list = ko_word_list.find_all('span', class_="txt_mean")
            ko_word_1 = span_mean_list[0].get_text(strip=True)
            if ko_word_1 is None:
                ko_word_1 = self.__none_str
        except Exception as e:
            print(repr(e))
        return ko_word_1

    def __get_ko_word_2(self, inner_top):
        ko_word_2 = self.__none_str
        try:
            ko_word_list = inner_top.find("ul", class_='list_mean')
            span_mean_list = ko_word_list.find_all('span', class_="txt_mean")
            ko_word_2_list = []
            if len(span_mean_list) > 1:
                for span_mean in span_mean_list:
                    ko_word_2_list.append(span_mean.get_text(strip=True))
                ko_word_2_list.pop(0)
                ko_word_2 = self.__join_str.join(ko_word_2_list)
        except Exception as e:
            print(repr(e))
        return ko_word_2

    def __get_en_phonetic(self, inner_top):
        en_phonetic = self.__none_str
        try:
            en_phonetic_tag = inner_top.find_all('span', class_='txt_pronounce')
            en_phonetic_list = []
            for en_phonetic in en_phonetic_tag:
                en_phonetic_list.append(en_phonetic.get_text(strip=True).replace("[", "").replace("]", ""))
            en_phonetic = self.__join_str.join(en_phonetic_list)
        except Exception as e:
            print(repr(e))
        return en_phonetic

    def __get_word_class(self, card_sort):
        word_class = self.__none_str
        try:
            word_class_tag = card_sort.find_all('strong')
            word_class_list = []
            for word_class in word_class_tag:
                word_class_list.append(word_class.get_text(strip=True))
            word_class = self.__join_str.join(word_class_list)
        except Exception as e:
            print(repr(e))
        return word_class

        # 한글 발음 크롤링

    def __get_ko_phonetic(self, s_word):
        ko_phonetic = self.__none_str
        try:
            ko_phonetic_url = f"http://aha-dic.com/View.asp?word={s_word}"
            resp = requests.get(ko_phonetic_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            ko_phonetic_tag = soup.find('span', class_="phoneticKor")
            ko_phonetic = ko_phonetic_tag.get_text(strip=True).replace("[", "").replace("]", "")
        except Exception as e:
            print(repr(e))
        return ko_phonetic

    # 한글 로마자 표기 크롤링
    def __get_ko_romanize(self, ko_word_1):
        ko_romanize = self.__none_str
        try:
            ko_romanize_url = f"http://roman.cs.pusan.ac.kr/result_all.aspx?input={ko_word_1}"
            resp = requests.get(ko_romanize_url)
            soup = BeautifulSoup(resp.text, 'html.parser')
            ko_romanize_tag = soup.select('td.td2')
            ko_romanize = ko_romanize_tag[len(ko_romanize_tag) - 1].get_text(strip=True).replace("①", "")
        except Exception as e:
            print(repr(e))
        return ko_romanize

    def get_word_dict(self):
        if self.__is_get_detail_page:
            en_phonetic = self.__get_en_phonetic(self.__inner_top)
            word_class = self.__get_word_class(self.__card_sort)
            ko_phonetic = self.__get_ko_phonetic(self.__word)
            ko_word_1 = self.__get_ko_word_1(self.__inner_top)
            ko_word_2 = self.__get_ko_word_2(self.__inner_top)
            ko_romanize = self.__get_ko_romanize(ko_word_1)
            word = {'is_success': self.__is_get_detail_page,
                    'en_word': self.__word,
                    'en_phonetic': en_phonetic,
                    'word_class': word_class,
                    'ko_phonetic': ko_phonetic,
                    'ko_word_1': ko_word_1,
                    'ko_word_2': ko_word_2,
                    'ko_romanize': ko_romanize,
                    }
        else:
            word = {'is_success': self.__is_get_detail_page}

        return word







if __name__ == '__main__':
    daum_dict = DaumDict("good")
    if daum_dict.is_get_detail_page():
        print(daum_dict.get_word_dict())

