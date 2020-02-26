function switchFunction() {
    var checkBox = document.getElementById("SwitchOptionDefault");
    var passfield = document.getElementById("passfield");
    var roompass = document.getElementById("roompass");
    if (checkBox.checked == true){
      passfield.style.display = "block";
    } else {
       passfield.style.display = "none";
       roompass.value = "";
    }
}
