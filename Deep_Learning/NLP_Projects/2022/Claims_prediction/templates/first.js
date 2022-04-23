var username = prompt("What is your name?");
alert( "Welcome " + username + ", Please type in the box and press the click button")


function Enter(){
var myValue = document.getElementById('TextBox').value;{
if( myValue.length == 0){
    alert(username + ', Please enter a value in the box');
    return;
}

var myTitle = document.getElementById('Title');
myTitle.innerHTML = myValue;
}
}