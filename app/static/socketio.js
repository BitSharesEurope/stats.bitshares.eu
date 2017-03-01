var namespace = 'status';
var room = window.location.hash.substring(1) || "bts";
var conn_options = {
    'sync disconnect on unload':true,
    resource:'socket.io'
};

//socket = io(window.location.href + namespace, conn_options);
socket = io("http://stats.bitshares.eu/" + namespace, conn_options);

function connectToNetwork() {
    console.log("connecting...");
    socket.emit("connect", {});

    socket.on('log', function(msg) {
        console.log(msg.msg);
    });

    socket.on('init', function(msg) {
        console.log("init graph " + msg.length);
        var series1 = [];
        var series2 = [];
        for (var i = 0; i < msg.length; i++)
        {
            series1.push({
             x: msg[i][0] * 1000,
             y: msg[i][2],
             block: msg[i][3]
            });
            series2.push({
             x: msg[i][0] * 1000,
             y: msg[i][1],
             block: msg[i][3]
            });
        }
        hchart.series[0].setData(series1);
        hchart.series[1].setData(series2);
    });

    /*
    socket.on('notice', function(msg) {
        hchart.series[0].addPoint({
         x: msg["timestamp"] * 1000,
         y: msg["num_transactions"],
         block: msg["block"]
        }, true);
        hchart.series[1].addPoint({
         y: msg["timestamp"] * 1000,
         y: msg["num_operations"],
         block: msg["block"]
        }, true);
    });
   */

    socket.on('connect', function() {
        console.log("connected");
        socket.emit("join", room);
    });
}

$(document).ready(function(){
    connectToNetwork();
});
