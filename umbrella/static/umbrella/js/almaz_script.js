// Мои личные скрипты для Umbrella

// ==================== Нажатие на главной странице связатся с нами ========================
const contact_us = document.getElementById("send_114")
contact_us.addEventListener("click", function(event) {
      console.log("clicked !");
      // console.log($('input[name=csrfmiddlewaretoken]').val());
      // console.log(document.getElementById("input_email").value);

      $.ajax({
        type:'POST',
        url:'http://127.0.0.1:8000/umbrella/main',                       // адрес откуда будем брать данные/откуда запрос идет
        data:{
            csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
            email_value : document.getElementById("input_email").value,
            action: 'ajax_send_zayvka'                              // присвоим action - свое имя
        },
        success:function(data){
        alert(data)
        },
        error : function(xhr,errmsg,err) {
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
            " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    }
    });

})

// *****************************************************
//<!-- Сохраняем заявку от пользователя на приобретение продукта с сайта в БД -->
// {

// $(document).on('submit', '#send_zayvka_1',function(e){      // отслеживаем событие отправки формы через его id
//     e.preventDefault();
//     console.log('clicked 2');
//     // создаем AJAX-вызов
//     $.ajax({
//         type:'POST',
//         url:'{% url "main" %}',                       // адрес откуда будем брать данные/откуда запрос идет
//         data:{
//             csrfmiddlewaretoken:$('input[name=csrfmiddlewaretoken]').val(),
//             email_value : document.querySelector('#input_email'),
// //            selected_year : document.querySelector('#select_year_2').selectedOptions[0].text,
//             action: 'ajax_send_zayvka'                              // присвоим action - свое имя
//         },
//         success:function(data){
//         alert(data)
//         },
//         error : function(xhr,errmsg,err) {
//         $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg+
//             " <a href='#' class='close'>&times;</a></div>"); // add the error to the dom
//         console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
//     }
//     });
// });

// }