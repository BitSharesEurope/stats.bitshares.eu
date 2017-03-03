var chart = new CanvasJS.Chart("hchart",{
 height: 550, //in pixels
 axisX:{
  labelFontSize: 12,
  labelAngle: -60,
 },
 zoomEnabled: true,
 axisY:{
  labelFontSize: 12,
 },
 data: [{
  type: "line",
  showInLegend: true,
  legendText: "Operations",
  toolTipContent: '<b>Operations</b><br />Block: <a href="https://cryptofresh.com/b/{block}">#{block}</a><br /># Ops: {y}',
  xValueType: "dateTime",
  dataPoints: []
 }, {
  type: "line",
  showInLegend: true,
  legendText: "Transactions",
  toolTipContent: '<b>Transactions</b><br />Block: <a href="https://cryptofresh.com/b/{block}">#{block}</a><br /># Txs: {y}',
  xValueType: "dateTime",
  dataPoints: []
 }]
});
