
var currentStateVal = 0;
var dateVal = 0;
$( document ).ready(function() {
    console.log( "ready!" );
    $('.calendar').datepicker();
    $('button').click(function(event) {
        dateVal = $('#calendar').val(); 
    })
    $('.dropdown-menu a').on('click', function(){  
        console.log($(this).data("value"));
        currentStateVal = $(this).data("value");
        $('.dropdown-toggle').html($(this).html());    
    })
    $.getJSON("https://vandyhacks-1541273118069.firebaseapp.com/StoreLocator.json", function(json) {
        console.log(json); // this will show the info it in firebug console
    });
//    console.log(csvJSON());

});
var map;
function initMap() {
        map = new google.maps.Map(document.getElementById('map'), {
          center: {lat: -34.397, lng: 150.644},
          zoom: 8
        });
}
