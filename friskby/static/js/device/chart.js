function createDeviceChart( chart_id , title) {
    var ctx = document.getElementById(chart_id);

    var chart = new Highcharts.Chart({
	chart: {
            renderTo: ctx,
            type: 'line',
            backgroundColor: 'transparent',
            zoomType: 'xy'},
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
	title : {
	    text : title
	},
	yAxis: {
            title: {
		text: 'μg/m3'
            },
            min: 0,
            max: 100
	}
    });

    return chart;
}
		      
