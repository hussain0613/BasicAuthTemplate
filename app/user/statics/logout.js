function logout(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    
    xhttp.open("get", "http://127.0.0.1:8000/user/api/logout/", true);
    
    xhttp.send();
}