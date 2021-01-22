var userEmail;
var userPassword;
    
function input(){
    userEmail = document.getElementById("email").value;
    userPassword = document.getElementById("password").value;
    		
    if (userEmail == '' ||  userPassword == ''){
        alert('이메일과 비밀번호를 입력해주세요.');
    }
    else{
        window.location.href = 'http://softcon.ga/redirect?to=login&email='+userEmail+'&password='+userPassword;
    }
}

function enterkey(){
    if (window.event.keyCode == 13){
        input();
    }
}
