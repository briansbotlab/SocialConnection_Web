$("#secrchUser").bind('input propertychange', function() {
      var keyword = $(this).val();
      var url = "/static/images/ic_launcher.png";
      $.ajax({
        url: '/main/Users/search/',
        data: {
          'keyword': keyword
        },
        type: 'GET',
        dataType: 'json',
        success: function (data) {
          $("#users").html("");
          if (data == ''){
            $("#users").append(
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

               if (item.imageURL == "default"){
                $("#users").append(
                  "<div class="+'chat_list'+">"+
                    "<div class="+'chat_people'+">"+
                      "<div class="+'chat_img'+">"+
                      "<img class="+'img-circle' +" src="+ url+" alt="+'ic_launcher.png' +">"+
                        "</div>"+
                       "<div class="+'chat_ib'+">"+
                         "<h5>"+item.username+"</h5>"+
                       "</div>"+
                     "</div>"+
                   "</div>"
              );
               }else {
                 $("#users").append(
                   "<div class="+'chat_list'+">"+
                     "<div class="+'chat_people'+">"+
                       "<div class="+'chat_img'+">"+
                        "<img src="+item.imageURL+" alt="+'image'+" class="+'img-circle'+">"+
                        "</div>"+
                       "<div class="+'chat_ib'+">"+
                         "<h5>"+item.username+"</h5>"+
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
