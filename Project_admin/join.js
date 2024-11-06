const form = document.getElementById("form")

form.addEventListener("submit", function(e){
  e.preventDefault();

  let userId = e.target.id.value
  let userPw1 = e.target.pw1.value
  let userPw2 = e.target.pw2.value
  let userName = e.target.name.value
  let userPhone = e.target.phone.value
  let userCategory = e.target.category.value
  let userGender = e.target.gender.value
  let userEmail = e.target.email.value

  console.log(userId, userPw1, userPw2, userName,
    userPhone, userCategory, userGender, userEmail)

  if(userId.length < 6){
    alert("아이디가 너무 짧습니다. 6자 이상 입력해주세요.")
    return;
  }

  if(userPw1 !== userPw2){
    alert("비밀번호가 일치하지 않습니다.")
    return;
  }

  document.body.innerHTML = ""
  document.write(`<p>${userId}님 환영합니다 <br> 회원가입 시 입력하신 내용은 다음과 같습니다. <br> 
    아이디 : ${userId} <br>
    이름 : ${userName} <br>
    전화번호 : ${userPhone} <br>
    선호하는 카테고리 : ${userCategory} <br>
    가입해 주셔서 감사합니다.
    </p> `)
})