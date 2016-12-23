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
          },
          plotLines: [{
              color: '#FF0000',
              width: 5,
              value: Date.parse(values[0]["pm25list"][0]["timestamp"])
          }]
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

    });
    return {
      select: function(id) {
        console.log("selecting in chart: " + id);
        chart.series.forEach(function(s) {s.hide();});
        var ser = chart.get(id)
        console.log(ser);
        ser.show();
      },
      showDataFor(values, key) {
           values.forEach(function(sensor) {
              chart.addSeries({
                id: sensor.id,
                name: sensor.locname,
                //color: '#F33',
                data: sensor[key].map(function(measurement) {
                  return [Date.parse(measurement.timestamp),
                          measurement.value];
                })
              });
          });
      }
    };
}
