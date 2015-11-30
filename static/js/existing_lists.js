function showPosition(position){
    console.log(position);
    var lat = position.coords.latitude;
    var lon = position.coords.longitude;
    console.log(lat,lon);
    var postParams = { 'lat' : lat, 'lon' : lon};
    console.log(postParams)
    $.get('/location', postParams, function() {
        console.log("we're back")});
};


navigator.geolocation.getCurrentPosition(showPosition);