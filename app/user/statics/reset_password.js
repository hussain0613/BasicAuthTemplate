function reset_password(){
    email = document.getElementById('email').value
    password = document.getElementById('password').value
    token = document.getElementById('token').value
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    
    xhttp.open("put", "http://127.0.0.1:8000/user/api/reset_password/?token="+token, true);
    
    xhttp.send(
        JSON.stringify({
            'email': email,
            'password': password,
        })
    );
    return false;
}