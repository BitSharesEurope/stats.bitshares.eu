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
        chart.options.data[0].dataPoints = series2;
        chart.options.data[1].dataPoints = series1;
        chart.render();		
    });

    socket.on('notice', function(msg) {
        chart.options.data[1].dataPoints.push({
         x: msg["timestamp"] * 1000,
         y: msg["num_operations"],
         block: msg["block"], 
        });
        chart.options.data[0].dataPoints.push({
         x: msg["timestamp"] * 1000,
         y: msg["num_transactions"],
         block: msg["block"], 
        });
        chart.options.data[0].dataPoints.shift();				
        chart.options.data[1].dataPoints.shift();				
        chart.render();		

        var date = new Date(msg["timestamp"] * 1000);
        $("#time").html(date.toLocaleTimeString());
    });

    socket.on('stats', function(d) {
       $("#max_num_ops").html(
        d["max_num_ops"].toLocaleString() + " ops/block" +
        "<br/>" + (d["max_num_ops"]/3).toFixed(2).toLocaleString() + " ops/sec"
       );
       $("#max_num_txs").html(
        d["max_num_txs"].toLocaleString() + " txs/block" +
        "<br/>" + (d["max_num_txs"]/3).toFixed(2).toLocaleString() + " txs/sec"
       );
       $("#sum_ops").html(d["sum_ops"].toLocaleString());
       $("#sum_txs").html(d["sum_txs"].toLocaleString());

       $("#avg_ops_100").html(
        d["avg_ops_100"].toLocaleString() + " ops/block" +
        "<br/>" + (d["avg_ops_100"]/3).toFixed(2).toLocaleString() + " ops/sec"
       );
       $("#avg_txs_100").html(
        d["avg_txs_100"].toLocaleString() + " txs/block" +
        "<br/>" + (d["avg_txs_100"]/3).toFixed(2).toLocaleString() + " txs/sec"
       );
    });

    socket.on('connect', function() {
        console.log("connected");
        socket.emit("join", room);
        socket.emit("stats", room);
    });

    setInterval(function(){
         socket.emit("stats", room);
    }, 5000);
}

$(document).ready(function(){
    connectToNetwork();
});
