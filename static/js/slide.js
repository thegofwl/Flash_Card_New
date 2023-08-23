const wordElement = document.querySelector('.word');

function updateWord(newWord) {
  wordElement.textContent = newWord;
}

function fetchNewWord() {
  fetch('/api/words/') // 단어를 가져올 API URL
    .then(response => response.json())
    .then(data => {
      if (data.length > 0) {
        updateWord(data[0].word); // 단어 필드명 변경 필요
      }
    });
}

// 페이지 로드시 초기 단어 표시
fetchNewWord();

let slideInterval;

function startSlide() {
  fetchNewWord(); // 초기 단어 표시

  setTimeout(() => {
    clearInterval(slideInterval); // 이전 인터벌 해제
    slideInterval = setInterval(fetchNewWord, 500); // 0.5초 간격으로 단어 업데이트
  }, 3000); // 3초 후에 0.5초 간격으로 업데이트 시작
}

slideInterval = setInterval(startSlide, 4000); // 4초 간격으로 슬라이드 시작
