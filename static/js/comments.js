var options = {
  //Boolean - Whether to show lines for each scale point
  scaleShowLine : true,
  //Boolean - Whether we show the angle lines out of the radar
  angleShowLineOut : true,
  //Boolean - Whether to show labels on the scale
  scaleShowLabels : false,
  // Boolean - Whether the scale should begin at zero
  scaleBeginAtZero : true,
  //String - Colour of the angle line
  angleLineColor : "rgba(0,0,0,.1)",
  //Number - Pixel width of the angle line
  angleLineWidth : 1,
  //String - Point label font declaration
  pointLabelFontFamily : "'Arial'",
  //String - Point label font weight
  pointLabelFontStyle : "normal",
  //Number - Point label font size in pixels
  pointLabelFontSize : 12,
  //String - Point label font colour
  pointLabelFontColor : "#555",
  //Boolean - Whether to show a dot for each point
  pointDot : true,
  //Number - Radius of each point dot in pixels
  pointDotRadius : 3,
  //Number - Pixel width of point dot stroke
  pointDotStrokeWidth : 1,
  //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
  pointHitDetectionRadius : 20,
  //Boolean - Whether to show a stroke for datasets
  datasetStroke : true,
  //Number - Pixel width of dataset stroke
  datasetStrokeWidth : 2,
  //Boolean - Whether to fill the dataset with a colour
  datasetFill : true,
  //String - A legend template
  // legendTemplate : "<ul class=\"<%=name.toLowerCase()%>-legend\"><% for (var i=0; i<datasets.length; i++){%><li><span style=\"background-color:<%=datasets[i].strokeColor%>\"></span><%if(datasets[i].label){%><%=datasets[i].label%><%}%></li><%}%></ul>"
};
function show_rating_graph(event_id, presenter) {
  $.get('/comment/api/' + event_id + '/' + presenter, function(rating) {
    var data = {
      labels: rating.labels,
      datasets: [
        {
          label: "Reco Study Rating",
          fillColor: "rgba(120,220,220,0.2)",
          strokeColor: "rgba(100,220,220,1)",
          pointColor: "rgba(200,220,220,1)",
          pointStrokeColor: "#aff",
          pointHighlightFill: "#aff",
          pointHighlightStroke: "rgba(220,220,220,1)",
          data: rating.data
        }
      ]
    };
    var ctx = document.getElementById("ratingChart").getContext("2d");
    var myRadarChart = new Chart(ctx).Radar(data, options);
  });
};
