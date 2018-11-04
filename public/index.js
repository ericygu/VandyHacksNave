
var currentStateVal = 0;
var dateVal = 0;
var apiString = 0;
var month = 0;
var day = 0;
var statesInUS = ["AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV","WI","WY"] //ALL STATES IN USA
//var longitudeStorLocations = [];
//var latitudeStorLocations = [];
var jsonStoreLocations = null;
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
    $.getJSON("StoreLocatore.json", function(json) {
            console.log(json.length);
            jsonStoreLocations = json
//            for(var i = 0; i < json.length; i++){
//                longitudeStorLocations.push(json[i].longitude);
//                latitudeStorLocations.push(json[i].latitude);
//            }
            addMarkers();
    });
    
    //START CANVASJS CODE
    
});
var map;
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 39.83333333, lng: -98.58333333},
        zoom: 5
    });
//    var place = {lat: 39.83333333, lng: -98.58333333};
//    var marker = new google.maps.Marker({position: place, map: map});
}
function addMarkers(){
    for(var i = 0; i < jsonStoreLocations.length; i++){
        var place = {lat: json[i].latitude, lng: json[i].longitude};
        var marker = new google.maps.Marker({position: place, map: map});
        var 
        
    }
    var markerCluster = new MarkerClusterer(map, markers,
            {imagePath: 'https://developers.google.com/maps/documentation/javascript/examples/markerclusterer/m'});
    
}
