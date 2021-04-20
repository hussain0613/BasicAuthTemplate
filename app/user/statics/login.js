function login(){
    username = document.getElementById('username').value
    password = document.getElementById('password').value
    remember_me = document.getElementById('remember_me').checked
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    
    xhttp.open("put", "http://127.0.0.1:8000/user/api/token/", true);
    
    xhttp.send(
        JSON.stringify({
            'username': username,
            'password': password,
            'remember_me': remember_me
        })
    );
    return false;
}