var hchart = null;
var series = {};
series.name = 'Throuput';
series.data = [];
$('#hchart').highcharts({
    chart: {
        type: 'spline',
        animation: Highcharts.svg, // don't animate in old IE
        events: {
            load: function () {
                hchart = this;
            }
        },
    },
    xAxis: {
        type: 'datetime',
        tickPixelInterval: 150
    },
    yAxis: {
        title: {
            text: 'Transactions/Operations per Bblock'
        },
    },
    series: [
        {name:"transactions"},
        {name:"operations"},
    ],
    colors: ['#7cb5ec', '#ff8528', '#90ed7d', '#f7a35c', '#8085e9',
             '#f15c80', '#e4d354', '#8085e8', '#8d4653', '#91e8e1'
    ],
    rangeSelector:{
        enabled: true,
    },
    navigator:{
        enabled: true
    },
    title: {
        text: 'Throughput'
    },
    tooltip: {
        formatter: function () {
            return '<b>' +
                this.series.name +
                '</b><br/>' +
                Highcharts.dateFormat('%Y-%m-%d %H:%M:%S', this.x) +
                ' (#' +
                this.point.block +
                ')' +
                '<br/>' +
                '<b>T/O per second:</b> ' +
                (Highcharts.numberFormat(this.y, 2) / 3).toFixed(2);
        }
    },
    legend: {
        enabled: true
    },
    exporting: {
        enabled: false
    },
    credits: {
        enabled: false
    }
});
