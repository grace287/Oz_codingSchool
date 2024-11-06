  // 현재 날짜와 시간을 표시하는 함수
  function displayCurrentDatetime() {
    const now = new Date();
    const options = { year: 'numeric', month: '2-digit', day: '2-digit', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
    const formattedDatetime = now.toLocaleString('ko-KR', options);
    document.getElementById('current-datetime').innerText = `현재 날짜 및 시간: ${formattedDatetime}`;
}