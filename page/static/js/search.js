var keyword
function search() {
    keyword = document.getElementById("search_field").value;
    window.location.href = "http://117.16.137.17:8000/search?key=" + keyword;
}

function enterkey() {
    if (window.event.keyCode == 13) {
        keyword = document.getElementById("search_field").value;
        window.location.href = "http://117.16.137.17:8000/search?key=" + keyword;
    }
}
