function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}


var elements = document.getElementsByClassName("msg");
for (var i = 0, len = elements.length; i < len; i++) {
    elements[i].innerHTML = urlify(element.innerHTML);
}
