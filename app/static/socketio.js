var namespace = 'status';
var room = "bts";
var conn_options = {
    'sync disconnect on unload':true,
    resource:'socket.io'
};

socket = io(window.location.href + namespace, conn_options);

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
            series1.push([msg[i][0] * 1000, msg[i][2]]);
            series2.push([msg[i][0] * 1000, msg[i][1]]);
        }
        hchart.series[0].setData(series1);
        hchart.series[1].setData(series2);
    });

    socket.on('notice', function(msg) {
        hchart.series[0].addPoint([
            msg["timestamp"] * 1000,
            msg["num_transactions"]
        ], true);
        hchart.series[1].addPoint([
            msg["timestamp"] * 1000,
            msg["num_operations"]
        ], true);
    });

    socket.on('connect', function() {
        console.log("connected");
        socket.emit("join", room);
    });
}

$(document).ready(function(){
    connectToNetwork();
});
