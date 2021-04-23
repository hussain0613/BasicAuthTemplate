function signup(){
    name_ = document.getElementById('name').value
    username = document.getElementById('username').value
    email = document.getElementById('email').value
    password = document.getElementById('password').value
    token = document.getElementById('token').value
    console.log(token)
    
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("demo").innerHTML = this.responseText;
        }
    };
    
    xhttp.open("post", "http://127.0.0.1:8000/user/api/signup/?token="+token, true);
    
    xhttp.send(
        JSON.stringify({
            'name': name_,
            'username': username,
            'email': email,
            'password': password,
        })
    );
    return false;
}