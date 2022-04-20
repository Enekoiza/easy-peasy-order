
//A function that returns the cookie's value
function getCookie(name) {
    var cookie = document.cookie;
    var prefix = name + "=";
    var begin = cookie.indexOf("; " + prefix);
    if (begin == -1) {
        begin = cookie.indexOf(prefix);
        if (begin != 0) return null;
    } else {
        begin += 2;
        var end = document.cookie.indexOf(";", begin);
        if (end == -1) {
        end = cookie.length;
        }
    }
    return unescape(cookie.substring(begin + prefix.length, end));
  }

//Open the language modal show when the flag is clicked
$(document).ready(function(){
    $('#language-flag').click(function() {
        $('#modal-language').modal("show");
    });
});

//Save in the local storage the flag and language that will be used in the speech to text conversion,
// so it keeps permanents while switching between the different views
$(document).ready(function () {
    if(localStorage.length == 0)
    {
      localStorage.setItem('language-url', $('#language-flag').attr('src'));
      localStorage.setItem('language', $('#language-flag').val());
    }
    selected_flag = localStorage.getItem('language-url');
    $('#language-flag').attr('src', selected_flag);
    $('.language-modal-body input').click(function() {
      var selected_flag_URL = $(this).attr('src');
      var selected_language = $(this).val();
      localStorage.setItem('language-url', selected_flag_URL);
      localStorage.setItem('language', selected_language);
      $('#language-flag').attr('src', selected_flag_URL);
      $('#modal-language').modal('toggle');
    });
});


//Delete items in the basket and update the basket
$(document).on('click', '.delete-button', function(){
    var IDholder = $(this).attr("id");

    var costQ = JSON.parse(localStorage.getItem(IDholder));

    var priceGap = parseFloat(costQ[0]).toFixed(2) * parseFloat(costQ[1]);

    var totalPrice = $('#final-price').text();

    totalPrice = totalPrice.replace(/[£,]/g, '');

    totalPrice = parseFloat(totalPrice) - priceGap;

    $('#final-price').text('£' + totalPrice.toFixed(2));

    localStorage.removeItem(IDholder);
    $(this).closest('.delete-parent').remove();
    basket_lenght = localStorage.length - 2;
    if(basket_lenght == 0)
    {
      $('#addToCart').text("View Basket (Empty)");

    }
    else{
      $('#addToCart').text("View Basket (" + basket_lenght + " item/s)");
    }
    
});

//Clean the modal basket build it with the local storage information and show the modal
$(document).ready(function(){
    $('#addToCart').click(function(){
        $('.modal-body-basket').empty();
        var finalCost = 0;
        for(var i = 0; i < localStorage.length; i++){
            var key = localStorage.key(i);
            if((key == "language") || (key == "language-url"))
            {
              continue;
            }
            var value = JSON.parse(localStorage.getItem(key));
            // alert(value);
            $('.modal-body-basket').append('<div class="delete-parent" id=' + key + '><p class="d-block" style="float:left;">' + key + ' => ' + 
            value[0] + '</p><button class="delete-button" style="float:left; margin-left:10px;" id="' + key + '" type="button">X</button></div>');

            finalCost = parseFloat(finalCost) + (parseFloat(value[0]) * parseFloat(value[1]));
            finalCost = parseFloat(finalCost).toFixed(2);
        }
            finalCost = '£' + finalCost.toString();
            $('.modal-body-basket').append('<label for="final-price">Final cost:</label>')
            
            $('.modal-body-basket').append('<h1 id="final-price">' + finalCost + '</h1>')

        $('#basket-modal').modal("show");
    });

})

//Live search
$(document).ready(function() {
    var search = $('#search').val();
    load_data(search);
    function load_data(query)
    {

        $.ajax({
            url:"/ajaxlivesearch",
            method:"POST",
            data:{query:query},
            success:function(data)
            {
                $('#result').html(data);
                $('#result').append(data.htmlresponse);

            }
        });
    }
    $('#search').keyup(function(){
        var search = $(this).val();
        if(search != ''){

            load_data(search);
        }
        else{

            load_data();
        }
    });

});

//Entrance cookie allowance modal
$(document).ready(function(){
    var now = new Date();
    var time = now.getTime();
    var expireTime = time + 1000*36000;
    now.setTime(expireTime);
    // Deny the close by clicking outside the window
    $('#modal-start').modal({
        backdrop: 'static',
        keyboard: false
    })
    var myCookie = getCookie("cookies");
    // No cookie store
    if (myCookie == null)
    {
        $('#modal-start').modal("show");
    }
    // Cookie stored
    else{
        return;
    }
    // Get started is pressed
    $('#get-started').click(function(){
        $('#modal-start').modal('toggle');
        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', './static/audio/welcome.mp3');
        audioElement.play();
        document.cookie = 'cookies=allow;expires='+now.toUTCString()+';path=/';
    });
    //Close is pressed
    $('.close-get-started').click(function(){
        var audioElement = document.createElement('audio');
        audioElement.setAttribute('src', './static/audio/welcome.mp3');
        audioElement.play();
        document.cookie = 'cookies=no-allow;expires='+now.toUTCString()+';path=/';
    });
});

//Generate a hidden input with all the basket information and pass it to the server side within a form
$(document).ready(function(){
    $('#pay-order').click(function(){
        
      var productCount = localStorage.length - 2;
      if(productCount == 0)
      {
          alert("The basket is empty");
          return;
      }
      $('#new-order').append('<input type="hidden" id="product-count" name="product-count" value="' + productCount + '">');
      var counter = 0;
      var i = 0;
      localHolder = parseInt(localStorage.length)
      while(localHolder > 2){


                var key = localStorage.key(i);
                var value = localStorage.getItem(key);
                
                if((key == "language") || (key == "language-url"))
                {
                    i = i + 1;
                    localHolder = parseInt(localStorage.length)
                  continue;
                }
                else{
                    temp = JSON.parse(value);
                    valueHolder = temp[0]
                    var productholder = "product" + counter.toString();
                    var productvalue = "product-value" + counter.toString();
                    $('#new-order').append('<input type="hidden" id="' + productholder + '" name="' + productholder + '" value="' + key + '">');
                    $('#new-order').append('<input type="hidden" id="' + productvalue + '" name="' + productvalue + '" value="' + valueHolder + '">');
                    counter++;
                    localStorage.removeItem(key);
                    i = 0;
                    localHolder = parseInt(localStorage.length)
                }

            }
            alert("The order has been stored.");
            $('#new-order').submit();

    });
  });

//Error message to represent a failure while receiving the voice message.
$(document).ready(function(){
    history.pushState(null, '', '/');
    var error = $('#hide-error').val();
    if(error == "ERROR")
    {
        alert('An error ocurred while detecting your voice, please give privileges to the microphone.');
        window.location.replace('/');
    }
});

$(document).ready(function(){
    var confidence = parseFloat($('#confidence').val());
    if (confidence < 0.7){
        alert("Sorry, the message matches are very low. Please carefully check that the word you said is the one inserted in the search bar.");
    }
})

