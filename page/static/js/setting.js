var userEmail;
var userPassword;

function ch() {
    passwd1 = document.getElementById("password").value;
    passwd2 = document.getElementById("password2").value;

    if (passwd1 != passwd2) {
        alert("비밀번호가 일치하지 않습니다.");
    } else {
        if (passwd1 == '') {
            alert("비밀번호를 입력해주세요.");
        }
        else {
            if (passwd1.length < 8) {
                alert("비밀번호는 8자 이상 입력해주세요.");
            }
            else {
		alert("비밀번호 변경이 완료되었습니다.");
                window.location.href = 'http://117.16.137.17:8000/redirect?to=changepw&password=' + passwd1;
            }
        }

    }
}
