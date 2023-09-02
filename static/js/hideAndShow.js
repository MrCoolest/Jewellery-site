function myfun(){
    const showIcon = document.getElementById("showIcon");
    const hideIcon = document.getElementById("hideIcon");
    const passwd = document.getElementById("passwd");

    if(passwd.type == "password"){
        passwd.type = "text";
        hideIcon.style.display = "none";
        showIcon.style.display = "block";
    }
    else{
        passwd.type = "password";
        hideIcon.style.display = "block";
        showIcon.style.display = "none";
    }
}