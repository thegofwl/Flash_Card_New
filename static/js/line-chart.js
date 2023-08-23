// line-chart.js

// 문서가 로드될 때 실행되는 함수
document.addEventListener('DOMContentLoaded', function() {
    var lineCtx = document.getElementById('lineChart').getContext('2d');

    // 데이터 예시 (가상의 데이터)
    var chartData = {
        labels: ['1회차', '2회차', '3회차', '4회차', '5회차'],
        datasets: [{
            label: '테스트 점수 경향',
            data: [50, 70, 35, 80, 90],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true
        }]
    };

    var lineChart = new Chart(lineCtx, {
        type: 'line', // 라인 차트 유형
        data: chartData,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                x: {
                    display: true,
                    title: {
                        display: true,
                        text: 'X 축 라벨'
                    }
                },
                y: {
                    display: true,
                    title: {
                        display: true,
                        text: 'Y 축 라벨'
                    }
                }
            }
        }
    });
});
