$(document).ready(function() {
  var i = 1;
  $('.add').on('click', function() {
    var field = '<br><input id="answer_"'+i+' class="md-textarea form-control" placeholder="Input '+i+'nd Answer Here" type="text"/>';
    $('.ans').append(field);
    i = i+1;
  })

  para_id = document.getElementById("paraid").innerText;
  $.ajax({
			data : {
				paraid : para_id,
			},
			type : 'POST',
			url : '/getQues'
		})
		.done(function(data) {

			if (data.error) {
        $(".alert").hide()
			}
			else {
        if (data.length > 0) {
          $(".alert").show()
          data.forEach(myFunction);
          function myFunction(item) {
              document.getElementById("quesResult").innerHTML += "<tr><td>"+item.quesid +"</td><td>"+item.ques_txt +"</td><td>"+item.ans_txt +"</td><td><a class=\"delete\" title=\"Delete\" data-toggle=\"tooltip\"><i class=\"material-icons\">&#xE872;</i></a></td></tr>";
            }
        } else {
          $(".alert").hide()
        }
			}
		});



  $('#exportAsJson_1').on('click', function(event) {

   paraid = document.getElementById("paraid").innerText;

   $.ajax({
     data : {
       paraid : paraid
     },
     type : 'GET',
     url : '/exportAsJson',
     beforeSend: function() {
     $('.alert').alert()
           $('#form-response').html("<img src=\"{{ url_for('static', filename='images/AjaxLoader.gif')}} \"/>");
           },
           complete: function () {
           // hide the preloader (progress bar)
           $('#form-response').html("");
           }
   })
   .done(function(data) {
     debugger;
     if (data.error) {
       $(".alert").hide()
     }
   });
   event.preventDefault();
  });

	$('#annotethis').on('click', function(event) {

    paraid = document.getElementById("paraid").innerText;
    var numItems = $('.ans').children('input').length;
    var ans_text = ""
    if (numItems > 1) {
      $('.ans input[type="text"]').each(function(i,e){
          // Do your magic here
          if (numItems == i){
            ans_text += e.value
          } else{
            ans_text += e.value+"|"
          }
      });
    } else {
      ans_text = $('#answer').val()
    }

    para_tit = $('#para_tit').val()

		$.ajax({
			data : {
				paraid : paraid,
				para_tit : para_tit,
				question : $('#question').val(),
				answer : ans_text
			},
			type : 'POST',
			url : '/annotThis',
			beforeSend: function() {
			$('.alert').alert()
            $('#form-response').html("<img src=\"{{ url_for('static', filename='images/AjaxLoader.gif')}} \"/>");
            },
            complete: function () {
            // hide the preloader (progress bar)
            $('#form-response').html("");
            }
		})
		.done(function(data) {
      debugger;
			if (data.error) {
        $(".alert").hide()
			}
			else {
          $(".alert").show()
          document.getElementById("quesResult").innerHTML +=  "<tr><td>"+data.ques_id +"</td><td>"+data.ques_text +"</td><td>"+data.ans_text +"</td><td><a class=\"delete\" title=\"Delete\" data-toggle=\"tooltip\"><i class=\"material-icons\">&#xE872;</i></a></td></tr>";

			}
		});
		event.preventDefault();
	});

	// Delete row on delete button click
	$(document).on("click", ".delete", function(){
	  var currentTr = $(this).parents("tr");
      quesid =  $(this).parents("tr").children('td:first').text().trim();
      alert(quesid)
<!--      $(this).parents("tr").remove();-->
      $.ajax({
        data : {
          ques_id : quesid,
        },
        type : 'POST',
        url : '/delQues'
      })
      .done(function(data) {
        if (data == "Record Deleted!") {
        debugger;
        $(currentTr).remove();

<!--        return false;-->
        <!--setInterval('refreshPage()', 5000);-->
         <!--setTimeout(function(){-->

                        <!--$("#quesResult").load(" #quesResult");-->
                     <!--}, 2000);-->

          <!--$(this).load(this);-->
          <!--$("#quesResult").load(" #quesResult");-->

        }
      });

    });

});

<!--function refreshPage() {-->
   <!-- location.reload(true);}-->