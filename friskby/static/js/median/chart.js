function createchart() {
  console.log("making chart");
  var ctx = document.getElementById("chart");
  var chart = new Highcharts.Chart({
      chart: {
          renderTo: ctx,
          type: 'line',
          backgroundColor: 'transparent',
          zoomType: 'xy'
      },
      title: {
          text: null
      },
      xAxis: {
          type: 'datetime',
          dateTimeLabelFormats: { // don't display the dummy year
              month: '%e. %b',
              year: '%b'
          },
          title: {
              text: 'Date'
          }
      },
      yAxis: {
          title: {
              text: 'μg/m3'
          },
          min: 0,
          max: 100
      },
      tooltip: {
          headerFormat: '<b>{series.name}</b><br>',
          pointFormat: '{point.x: %A, %b %e, %H:%M}: {point.y:.2f}'
      },

      plotOptions: {
          spline: {
              marker: {
                  enabled: true
              }
          }
      },

    });

    return {
      select: function(id) {
        chart.series.forEach(function(s) {s.hide();});
        var ser = chart.get(id);
        ser.show();
      },
      showDataFor: function(values, errors) {
          var plot_data = [];
          for (var i = 0; i < values.length; i++) {
              plot_data.push([Date.parse(values[i].timestamp_data), values[i].value]);
          }
          var plot_error = [];
          for (var i = 0; i < errors.length; i++) {
              var up = values[i].value + errors[i].value;
              var dn = values[i].value - errors[i].value;
              plot_error.push([Date.parse(values[i].timestamp_data), dn,up]);
          }
          chart.addSeries({
              type: 'spline',
              name: 'Bergen',
              data: plot_data
          });
          chart.addSeries({
              type: 'errorbar',
              data: plot_error
          });
      }
    };
}
