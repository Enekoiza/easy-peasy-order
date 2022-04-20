//Jquery to add the selected item to the localstorage in the front-end

$(document).ready(function(){

var basket_lenght = localStorage.length - 2;
if(basket_lenght > 0){
    $('#addToCart').text("View Basket (" + basket_lenght + " item/s)");

}
else{
    $('#addToCart').text("View Basket (Empty)");
}
$('#add-basket').click(function(){
    var product_info = $('.product-info-modal').text();
    var product_count = $('#item-count').text();
    var product_price = $('.product-cost-modal').text()
    product_price = product_price.replace(/[£,]/g, '');
    product_price = parseFloat(product_price) / parseInt(product_count);
    product_price = product_price.toFixed(2);
    var data = [parseInt(product_count), parseFloat(product_price)];
    if (localStorage.getItem(product_info) === null) {
    localStorage.setItem(product_info, JSON.stringify(data));
    basket_lenght = localStorage.length - 2;
    $('#product-modal').modal('toggle');
    $('#addToCart').text("View Basket (" + basket_lenght + " item/s)");
    }
    else{
    var data = JSON.parse(localStorage.getItem(product_info));
    data[0] = data[0] + parseInt(product_count);
    // var result = parseInt(count) + parseInt(product_count);
    localStorage.removeItem(product_info);
    localStorage.setItem(product_info, JSON.stringify(data));
    basket_lenght = localStorage.length - 2;

    $('#product-modal').modal('toggle');
    $('#addToCart').text("View Basket (" + basket_lenght + " item/s)");
    }

    
});
})


//Jquery to pop the modal when an item is clicked
$(document).ready(function(){
$("#product-group a").click(function(){
    var selected_product = $(this).find(".product-info").text();
    var selected_product_cost = $(this).find(".product-cost").text();
    var selected_product_image = $(this).find(".product-photo").prop('src');
    $('.product-info-modal').text(selected_product);
    $('.product-cost-modal').text(selected_product_cost);
    $('.product-photo-modal').attr('src', selected_product_image);
    $('#item-count').text(1);
    $('#product-modal').modal("show");
    return false;
})
})



//Jquery to add or remove 1 from the item counter inside the modal
$(document).ready(function(){
    $('#add-item-count').click(function(){  
        var cost = $('.product-cost-modal').text();
        var count = $('#item-count').text();
        var int_count = parseInt(count);
        cost = cost.replace(/[£,]/g, '');
        var productCost = (parseFloat(cost) / int_count).toFixed(1);
        int_count = int_count + 1;
        $('#item-count').text(int_count);
        var finalCost = productCost * int_count;
        finalCost = "£" + String(finalCost.toFixed(2));
        $('.product-cost-modal').text(finalCost);
    });
    $('#substract-item-count').click(function(){
        var cost = $('.product-cost-modal').text();
        cost = cost.replace(/[£,]/g, '');
        var count = $('#item-count').text();
        var int_count = parseInt(count);
        var productCost = (parseFloat(cost) / int_count).toFixed(1);
        int_count = int_count - 1;
        if(int_count < 1){
        alert("Sorry, you can't select less than 0");
        int_count = 1;
        $('#item-count').text(int_count);
        }
        var finalCost = productCost * int_count;
        finalCost = "£" + String(finalCost.toFixed(2));
        $('.product-cost-modal').text(finalCost);
        $('#item-count').text(int_count);
    });

})

//Jquery to close the modal when the .modal-closer class selector is clicked (the 'x' or the close button)
$(document).ready(function(){
    $('.modal-closer').click(function(){
        ('#product-modal').modal('toggle');
    });
})
