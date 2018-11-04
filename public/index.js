
var currentStateVal = 0;
var dateVal = 0;
var apiString = 0;
var month = 0;
var day = 0;
var longitudeStorLocations = [];
var latitudeStorLocations = [];
var marker = []
$( document ).ready(function() {
    console.log( "ready!" );
    $('.calendar').datepicker();
    $('button').click(function(event) {
        dateVal = $('#calendar').val(); 
        month = dateVal.slice(0,2);
   	    day = dateVal.slice(3,5);
        apiString = "s=" + currentStateVal + "&m=" + month + "&d=" + day;
    })
    $('.dropdown-menu a').on('click', function(){  
        currentStateVal = $(this).data("value");
        $('.dropdown-toggle').html($(this).html());    
    })
});
var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.83333333, lng: -98.58333333},
        zoom: 7
        $.getJSON("StoreLocatore.json", function(json) {
            console.log(json.length);
            for(var i = 0; i < json.length; i++){
                longitudeStorLocations.push(json[i].longitude);
                latitudeStorLocations.push(json[i].latitude);
                console.log(json[i].longitude)+" "+ json[i].latitude);
                var place = {lat: json[i].latitude, lng: json[i].longitude};
                marker[i] = new google.maps.Marker({position: place, map: map});
            }
        });
    });
}
