function show_loading() {
   $('#loading:hidden').show();
}
function kill_loading() {
   $('#loading:visible').hide();
}

function load_cameras(map) {
   $.getJSON('/cameras.json', function(response) {
      kill_loading();
      $.each(response.cameras, function(i, camera) {
         var marker = new google.maps.Marker({
            position: new google.maps.LatLng(camera.lat, camera.lng),
            title: camera.title,
            map: map});
         var content_html = '<p class="infowindow"><img src="';
         content_html += camera.link + '" alt="' + camera.title + '"/><br/>';
         content_html += '<strong>' + camera.title + '</strong></p>';
         
         var infowindow = new google.maps.InfoWindow({
            content: content_html
         });
         google.maps.event.addListener(marker, 'click', function() {
            infowindow.open(map,marker);
         });
         
      });
   });
}


/* START LOADING */

var browserSupportFlag =  new Boolean();
var max_nw = [51.69698,-0.602961];
var max_se = [51.251064,0.284357];
function initialize() {
   var latlng = new google.maps.LatLng(51.505377,-0.112438);
   var myOptions = {
zoom: 12,
      center: latlng,
      mapTypeId: google.maps.MapTypeId.ROADMAP
   };
   var map = new google.maps.Map(document.getElementById("map_canvas"), myOptions);
   
   // Try W3C Geolocation (Preferred)
   if(navigator.geolocation) {
      browserSupportFlag = true;
      navigator.geolocation.getCurrentPosition(function(position) {
         // only do this if it's somewhere near London
         if (position.coords.latitude > max_se[0] && position.coords.latitude < max_nw[0]
             && position.coords.longitude > max_nw[1] && position.coords.longitude > max_se[1])
           map.setCenter(new google.maps.LatLng(position.coords.latitude,position.coords.longitude));
      }, function() {
         handleNoGeolocation(browserSupportFlag);
      });
   }
   
   return map;
   
   
}

$(function() {
   var map = initialize();
   show_loading();
   load_cameras(map);
});