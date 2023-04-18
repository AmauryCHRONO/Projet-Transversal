var i = 0;
var h1 = 'Say hello to Drawbot. Your personal drawing robot.';
var speed = 40;

function typeWriter() {
  if (i < h1.length) {
    document.getElementById("sus").innerHTML += h1.charAt(i);
    i++;
    setTimeout(typeWriter, speed);}
  }

function flash(){
  if (document.getElementById("gog").value == ""){
    // something is wrong
      alert('There is a problem with the first field');
      return false;
    }
  return true;
  }
