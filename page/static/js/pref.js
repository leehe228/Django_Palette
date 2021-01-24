var v1 = "0";
var v2 = "0";
var v3 = "0";
var v4 = "0";
var v5 = "0";
var v6 = "0";
var v7 = "0";
var v8 = "0";
var v9 = "0";
var v10 = "0";

var s1 = false;
var s2 = false;
var s3 = false;
var s4 = false;
var s5 = false;
var s6 = false;
var s7 = false;
var s8 = false;
var s9 = false;
var s10 = false;

var d1 = document.getElementById("d1");
var d2 = document.getElementById("d2");
var d3 = document.getElementById("d3");
var d4 = document.getElementById("d4");
var d5 = document.getElementById("d5");
var d6 = document.getElementById("d6");
var d7 = document.getElementById("d7");
var d8 = document.getElementById("d8");
var d9 = document.getElementById("d9");
var d10 = document.getElementById("d10");

function add1() {
    if (s1 == false){
        d1.style.display = "none";
        s1 = true;
        v1 = "1";
    }
    else {
        d1.style.display = "";
        s1 = false;
        v1 = "0";
    }
}

function add2() {
    if (s2 == false){
        d2.style.display = "none";
        s2 = true;
        v2 = "1";
    }
    else {
        d2.style.display = "";
        s2 = false;
        v2 = "0";
    }
}

function add3() {
    if (s3 == false){
        d3.style.display = "none";
        s3 = true;
        v3 = "1";
    }
    else {
        d3.style.display = "";
        s3 = false;
        v3 = "0";
    }
}

function add4() {
    if (s4 == false){
        d4.style.display = "none";
        s4 = true;
        v4 = "1";
    }
    else {
        d4.style.display = "";
        s4 = false;
        v4 = "0";
    }
}

function add5() {
    if (s5 == false){
        d5.style.display = "none";
        s5 = true;
        v5 = "1";
    }
    else {
        d5.style.display = "";
        s5 = false;
        v5 = "0";
    }
}

function add6() {
    if (s6 == false){
        d6.style.display = "none";
        s6 = true;
        v6 = "1";
    }
    else {
        d6.style.display = "";
        s6 = false;
        v6 = "0";
    }
}

function add7() {
    if (s7 == false){
        d7.style.display = "none";
        s7 = true;
        v7 = "1";
    }
    else {
        d7.style.display = "";
        s7 = false;
        v7 = "0";
    }
}

function add8() {
    if (s8 == false){
        d8.style.display = "none";
        s8 = true;
        v8 = "1";
    }
    else {
        d8.style.display = "";
        s88 = false;
        v8 = "0";
    }
}

function add9() {
    if (s9 == false){
        d9.style.display = "none";
        s9 = true;
        v9 = "1";
    }
    else {
        d9.style.display = "";
        s9 = false;
        v9 = "0";
    }
}

function add10() {
    if (s10 == false){
        d10.style.display = "none";
        s10 = true;
        v10 = "1";
    }
    else {
        d10.style.display = "";
        s10 = false;
        v10 = "0";
    }
}

function save() {
    var v = v1 + v2 + v3 + v4 + v5 + v6 + v7 + v8 + v9 + v10; 

    location.href = 'http://softcon.ga/redirect?to=saveprf&v=' + v;
}
