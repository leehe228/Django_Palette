var userEmail;
var userPassword;
var name;
var age;
var genderButton;
var gender;

function openPrivacy() {
    window.open("http://softcon.ga/private_privacy/");
}

function CheckEmail(str) {
    var reg_email = /^([0-9a-zA-Z_\.-]+)@([0-9a-zA-Z_-]+)(\.[0-9a-zA-Z_-]+){1,2}$/;

    if (!reg_email.test(str)) {
        return false;
    }
    else {
        return true;
    }
}

function input() {
    userEmail = document.getElementById("email").value;
    userPassword = document.getElementById("password").value;
    userPassword2 = document.getElementById("password2").value;
    name = document.getElementById("name").value;
    age = document.getElementById("age").value;
    genderButton = document.getElementsByName("gender");

    if (genderButton[0].checked == true) {
        gender = "M"
    }
    else {
        gender = "W"
    }

    if (userEmail == '' || userPassword == '' || userPassword2 == '' || name == '' || age == '') {
        alert("모든 정보를 입력해주세요.");
    }
    else {
        if (!CheckEmail(userEmail)) {
            alert("올바른 이메일을 입력해주십시오.")
        }
        else {
            if (userPassword != userPassword2) {
                alert("비밀번호가 일치하지 않습니다.");
            } else {
                window.location.href = 'http://softcon.ga/redirect?to=signup&email=' + userEmail + '&password=' + userPassword + '&name=' + name + '&age=' + age + '&gender=' + gender;
            }
        }
    }
}


