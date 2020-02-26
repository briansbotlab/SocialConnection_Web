function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}

window.onload = function(){

  var elements = document.getElementsByClassName("msg");
  for (var i = 0, len = elements.length; i < len; i++) {
      elements[i].innerHTML = urlify(elements[i].innerHTML);
  }

var elem = document.getElementById('msg_history');
elem.scrollTop = elem.scrollHeight;

};

$('msg_history').bind("DOMSubtreeModified",function(){
  var elem = document.getElementById('msg_history');
  elem.scrollTop = elem.scrollHeight;
  alert('changed');
});
