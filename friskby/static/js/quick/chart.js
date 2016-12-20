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
          /*min: 0,
          max: 100*/
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
      series: values.map(function(sensor) {
        return {
          id: sensor.id,
          name: sensor.locname,
          color: '#F33',
          data: sensor["pm25list"].map(function(measurement) {
            return [Date.parse(measurement.timestamp),
                    measurement.value];
          })
        };
      })
    });
    return {
      select: function(id) {
        console.log("selecting in chart: " + id);
        chart.series.forEach(function(s) {s.hide();});
        var ser = chart.get(id)
        console.log(ser);
        ser.show();
      }
    };
}
