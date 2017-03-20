function createchart() {
  console.log("making chart");
  var default_plot = ["FriskPaiMorten", "FriskPI05", "FriskPI06", "FriskPI09", "FriskPI10",
                      "FriskPIFlikka", "FriskPiSasak"];
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
      showDataFor: function(values, key) {
        while(chart.series.length > 0)
           chart.series[0].remove(true);
         values.forEach(function(sensor) {
            chart.addSeries({
              id: sensor.id,
              name: sensor.locname,
              data: sensor[key].map(function(measurement) {
                return [Date.parse(measurement.timestamp_data),
                        measurement.value];
              }),
              visible: default_plot.indexOf(sensor.id)>=0
            });
        });
      },
      scrollTo: function(date) {
        chart.xAxis[0].removePlotBand("plotLine");

        chart.xAxis[0].addPlotLine({
                value: Date.parse(date),
                width: 3,
                color: 'red',
                id: "plotLine"
            });
      }
    };
}
