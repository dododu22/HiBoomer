
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var numbers_received = [];

    //receive details from server
    socket.on('html', function(msg) {
        console.log("Received number" + msg.number);
        //maintain a list of ten numbers
        $('#log').html(msg.number);
    });

});