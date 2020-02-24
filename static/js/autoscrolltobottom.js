window.onload = function(){
var elem = document.getElementById('msg_history');
elem.scrollTop = elem.scrollHeight;
};

$('msg_history').bind("DOMSubtreeModified",function(){
  var elem = document.getElementById('msg_history');
  elem.scrollTop = elem.scrollHeight;
  alert('changed');
});
