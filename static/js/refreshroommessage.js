//window.setInterval
//$(document).ready(function(){
//$("#msg_send_btn").click

function urlify(text) {
    var urlRegex = /(https?:\/\/[^\s]+)/g;
    return text.replace(urlRegex, function(url) {
        return '<a href="' + url + '">' + url + '</a>';
    })
    // or alternatively
    // return text.replace(urlRegex, '<a href="$1">$1</a>')
}

window.setInterval(function(){
    var roomid = document.getElementById('roomid').value;
    var userid = document.getElementById('userid').value;
    var url = "/static/images/ic_launcher.png";

    $.ajax({
      url: '/main/ChatRooms/'+roomid+'/interval/',
      data: {
        'roomid': roomid
      },
      type: 'GET',
      dataType: 'json',
      success: function (data) {

        var totalLength = 0;
        var last_msg_senttime = "";
        for (var i in data) {
          totalLength += 1;
          last_msg_senttime = data[i].senttime;
        }

        $("#msg_history").html("")
        if (data == ''){
            $("#msg_history").append("a");
        }else{
          $.each(data,function(index,item){

            if(item.sender != userid){
              var incoming_msg = document.createElement("div");
              incoming_msg.setAttribute("class", "incoming_msg");

              var incoming_msg_img = document.createElement("div");
              incoming_msg_img.setAttribute("class", "incoming_msg_img");
              $('#msg_history').append(incoming_msg);


              var innerHtml = "";

                  if(item.imageURL == "default"){
                    innerHtml = innerHtml +"<img class="+'img-circle' +" src="+ url+" alt="+'ic_launcher.png' +">";
                  }else{
                    innerHtml = innerHtml +"<img class="+'img-circle' +" src="+ item.imageURL+" alt="+'roomImg' +">";
                  }

              incoming_msg_img.innerHTML = innerHtml;

              var received_msg = document.createElement("div");
              received_msg.setAttribute("class", "received_msg");

              received_msg.innerHTML = "<p>" +item.sendername+"</p>";

              var received_withd_msg = document.createElement("div");
              received_withd_msg.setAttribute("class", "received_withd_msg");

              received_msg.appendChild(received_withd_msg);

              var innerHtml_2 = "";

                  if(item.type == "text"){
                    innerHtml_2 = innerHtml_2 +"<p class="+'msg'+">"+item.message+"</p>";
                  }else if (item.type == "image") {
                    innerHtml_2 = innerHtml_2 +"<img src="+ item.message +" alt="+'msgImage' +">";
                  }
                  innerHtml_2 = innerHtml_2 +"<span class="+'time_date_left'+">"+item.senttime+"</span>";
              received_withd_msg.innerHTML = innerHtml_2;

              incoming_msg.innerHTML = incoming_msg_img.outerHTML +received_msg.outerHTML ;
            }else{
              var outgoing_msg = document.createElement("div");
              outgoing_msg.setAttribute("class", "outgoing_msg");

              var sent_msg = document.createElement("div");
              sent_msg.setAttribute("class", "sent_msg");
              $('#msg_history').append(outgoing_msg);
              outgoing_msg.appendChild(sent_msg);

              var innerHtml = "";

                if(item.type == "text"){
                  innerHtml = innerHtml + "<p class="+'msg'+">"+item.message+"</p>" ;
                }else if (item.type == "image") {
                  innerHtml = innerHtml +"<img src="+ item.message+" alt="+'msgImage' +">";
                }
                innerHtml = innerHtml + "<span class="+'time_date'+">"+item.senttime ;



                  if(item.senttime == last_msg_senttime){
                    if(item.seennum > 0){
                      innerHtml = innerHtml +"<div class="+'seen'+"id="+'seen'+">"+"<br>Seen"+item.seennum+"</div>";

                    }else {
                      innerHtml = innerHtml +"<div class="+'seen'+"id="+'seen'+">"+"<br>Delivered"+"</div>";
                    }
                  }

                    sent_msg.innerHTML = innerHtml;

            }
          }
        )
        var elements = document.getElementsByClassName("msg");
        for (var i = 0, len = elements.length; i < len; i++) {
            elements[i].innerHTML = urlify(elements[i].innerHTML);
        }
        }


        //$('#msg_history').scrollTop($('#msg_history')[0].scrollHeight);
      },
      error:function(xhr){
        alert("發生錯誤: " + xhr.status + " " + xhr.statusText + " " + xhr.readyState);
      }
    });
//});
//});
}, 1000);
