$("#secrchRoom").bind('input propertychange', function() {
      var keyword = $(this).val();
      var url = "/static/images/ic_launcher.png";
      var lock = "/static/images/ic_lock_white_48dp.png"
      $.ajax({
        url: '/main/ChatRooms/search/',
        data: {
          'keyword': keyword
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
            //console.log(data);
          $("#rooms").html("")
          if (data == ''){
            $("#rooms").append(
              "<div class="+'chat_list'+">"+
                "<div class="+'chat_people'+">"+
                  "<div class="+'chat_img'+">"+
                  "<img class="+'img-circle' +" src="+ url+" alt="+'ic_launcher.png' +">"+
                    "</div>"+
                   "<div class="+'chat_ib'+">"+
                     "<h5>"+'No user data.'+"</h5>"+
                   "</div>"+
                 "</div>"+
               "</div>"
          );
          }else{
            $.each(data,function(index,item){
              console.log(item.id);

               if (item.imageURL == "default" && item.secret_status == "not_secret"){
                $("#rooms").append(
                  "<div class="+'chat_list'+">"+
                    "<div class="+'chat_people'+">"+
                      "<div class="+'chat_img'+">"+
                      "<img class="+'img-circle' +" src="+ url+" alt="+'ic_launcher.png' +">"+
                        "</div>"+
                       "<div class="+'chat_ib'+">"+
                         "<h5>"+item.chatRoomName+"</h5>"+
                       "</div>"+
                     "</div>"+
                   "</div>"
              );
            }else if(item.imageURL == "default" && item.secret_status == "secret"){
              $("#rooms").append(
                "<div class="+'chat_list'+">"+
                  "<div class="+'chat_people'+">"+
                    "<div class="+'chat_img'+">"+
                    "<img class="+'img-circle' +" src="+ url+" alt="+'ic_launcher.png' +">"+
                      "</div>"+
                     "<div class="+'chat_ib'+">"+
                       "<h5>"+item.chatRoomName+"</h5>"+
                     "</div>"+
                     "<div class="+'ic_lock'+">"+
                         "<img src="+ lock +" alt="+'ic_lock_white_48dp.png'+">"+
                     "</div>"+
                   "</div>"+
                 "</div>"
                 );
            }else if(item.secret_status == "not_secret"){
              $("#rooms").append(
                "<div class="+'chat_list'+">"+
                  "<div class="+'chat_people'+">"+
                    "<div class="+'chat_img'+">"+
                     "<img src="+item.imageURL+" alt="+'image'+" class="+'img-circle'+">"+
                     "</div>"+
                    "<div class="+'chat_ib'+">"+
                      "<h5>"+item.chatRoomName+"</h5>"+
                    "</div>"+
                   "</div>"+
                   "</div>"
                   );
            }else if(item.secret_status == "secret"){
                 $("#rooms").append(
                   "<div class="+'chat_list'+">"+
                     "<div class="+'chat_people'+">"+
                       "<div class="+'chat_img'+">"+
                        "<img src="+item.imageURL+" alt="+'image'+" class="+'img-circle'+">"+
                        "</div>"+
                       "<div class="+'chat_ib'+">"+
                         "<h5>"+item.chatRoomName+"</h5>"+
                       "</div>"+
                       "<div class="+'ic_lock'+">"+
                           "<img src="+ lock +" alt="+'ic_lock_white_48dp.png'+">"+
                       "</div>"+
                      "</div>"+
                      "</div>"
                 );
               }


            })
          }



        },
        error:function(xhr){
          alert("發生錯誤: " + xhr.status + " " + xhr.statusText + " " + xhr.readyState);
        }
      });
    });
