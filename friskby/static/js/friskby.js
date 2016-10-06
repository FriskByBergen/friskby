// The global namespace
/*var Friskby = (function( Friskby ) {
    return Friskby;
})( Friskby || {});*/
//var Friskby = Friskby || {};

/* Extends the Friskby namespace object with a load function */
var Friskby = (function() {
    /* Set if debug is active - default is false. */
    var debugActive = false;
    var _map;
    var _controller;
    var _view;
    var _model;
    var _chart;
    
    var load = function( isDebugging) {
        debugActive = isDebugging;
        
        debug("Friskby: loading map");
        _controller = Friskby.controller;
        _model = Friskby.model;
        _view = Friskby.view;
        _map = Friskby.olMap;
        _chart = Friskby.highcharts;
        
        _controller.setMap( _map );
        _map.load("map");
        
        _controller.setModel( _model );
        _controller.setChart( _chart );
        
        debug("Friskby will load after this..");
        _controller.populateModel();
    }
    
    var getMap = function() {
        return _map;
    }
    
    var getController = function() {
        return _controller;
    }
    
    var getView = function() {
        return _view;
    }
    
    var getModel = function() {
        return _model;
    }
    
    var getChart = function() {
        return _chart;
    }
    
    var debug = function( outputText ) {
        if( debugActive )
            console.log( outputText );
    }
    
    var debugging = function( isDebugging ) {
        debugActive = isDebugging;
    }
    
    return {
        debugging: debugging,
        load: load,
        map: getMap,
        controller: getController,
        chart: getChart,
        model: getModel
    } 
})();


var FriskbyModuleExtensions = (function ( Friskby ) {

    Friskby.model = (function () {
        "use strict";

        var _sensors = {};
        var _sensorTypes = {};
        var _devices = {};
        var _locations = {};
        var _measurementTypes = {};
        var _sensorInfos = {};
        var _timeSeries = {};
        var _timeSeriesGeoJSON = {};
        var _beginTime, _endTime;

        var apiUrl = {
            sensor:             "http://friskby.herokuapp.com/sensor/api/sensor/",
            sensorType:         "http://friskby.herokuapp.com/sensor/api/sensortype/",
            sensorInfo:         "http://friskby.herokuapp.com/sensor/api/sensorinfo/",
            device:             "http://friskby.herokuapp.com/sensor/api/device/",
            location:           "http://friskby.herokuapp.com/sensor/api/location/",
            measurementType:    "http://friskby.herokuapp.com/sensor/api/measurement_type/"
        }

        var apiUrlArray = function () {
            var keys = [], urls = [];
            $.each(apiUrl, function( key, val ) {
                keys.push(key);
                urls.push(val);
            });
            return {keys: keys, urls: urls}
        }

        var apiUrlTimeserie = function( sensorId ) {
            /* 2016-06-17T03:25:19.3Z */
            var daysAgo = new Date();
            daysAgo.setDate(daysAgo.getDate() - 6);
        
            return "http://friskby.herokuapp.com/sensor/api/reading/" + sensorId + "/?start=" + daysAgo.toISOString();
        }

        var apiUrlTimeseriesArray = function ( sensorTypes, numberOfMilliseconds ) {
            var keys = [], urls = [];
            $.each( _sensors, function( key, value ) {
                var correctType = $.inArray( value.sensor_type, sensorTypes );
                if( correctType >= 0 ) {
                    keys.push(key);
                    urls.push( apiUrlTimeserie( key ));
                }
            });
            return {keys: keys, urls: urls}
        }

         var getInfoHTML = function( sensorId ) {
             if( !_sensors.hasOwnProperty( sensorId ) ) 
                 return false;

             var tmpSensor = _sensorInfos[sensorId];
             
             if( tmpSensor.last_value == null )
                 return false;
             
             var div = $("<div></div>");
             div.addClass("fb-sensorInfo");
             div.addClass("fb-hiddenSensor");
             div.attr("id", sensorId );
             div.append("<h3>" + tmpSensor.parent_device.id + ": " + tmpSensor.sensor_type.short_description + "</h3><br/>");
             div.append("<span class='sensorType'>" + tmpSensor.sensor_type.description + ". </span>");
             div.append("It is placed at <span class='location'>" + tmpSensor.parent_device.location.name + "</span> at <span class='height'>" + tmpSensor.parent_device.location.altitude + "</span> m.a.s.l. ");
             div.append("Last value was at <span class='lastValue'>" + tmpSensor.last_value + " μg/m<sup>3</sup></span> " + Friskby.tools.timeDiffToHumanString(new Date(tmpSensor.last_timestamp), new Date()) + " ago."  );
             return div;
        }

        var getSensorTableRows = function() {
            var htmlString = "";
            var tmpDevices = {};
            var delDevices = [];

            $.each( _devices, function( key, device ) {
                tmpDevices[key] = {};
                tmpDevices[key].id = key;
                tmpDevices[key].location = device.location.name;
            });

            $.each( _sensors, function( key, sensor ) {
                if( _sensorInfos[sensor.id].last_value == null )
                    return "";
                
                if( sensor.sensor_type == 10 ) {
                    tmpDevices[sensor.parent_device]["PM10_id"] = sensor.id;
                    tmpDevices[sensor.parent_device]["PM10_value"] = Friskby.tools.round(_sensorInfos[sensor.id].last_value, 2);
                    tmpDevices[sensor.parent_device]["PM10_time"] = _sensorInfos[sensor.id].last_timestamp;
                }
                else if( sensor.sensor_type == 11 ) {
                    tmpDevices[sensor.parent_device]["PM25_id"] = sensor.id;
                    tmpDevices[sensor.parent_device]["PM25_value"] = Friskby.tools.round(_sensorInfos[sensor.id].last_value, 2);
                    tmpDevices[sensor.parent_device]["PM25_time"] = _sensorInfos[sensor.id].last_timestamp;
                }
            });

            $.each( tmpDevices, function( key, device ) {
               if( !device.hasOwnProperty("PM10_id") && !device.hasOwnProperty("PM25_id") )
                   delDevices.push(key);
            });

            $.each( delDevices, function( index, device ) {
                delete tmpDevices[device];       
            });

            $.each( tmpDevices, function( key, device ) {
                var timeDiff = Friskby.tools.timeDiffToHumanString(new Date( device.PM10_time ), new Date());
                if( device.PM10_time == null )
                    timeDiff = "-";
                htmlString += "<tr><td><a href='#' data-toggle='tooltip' data-placement='left' title='" + device.id + "'>" + device.location + "</a></td><td>" + device.PM25_value + "</td><td>" + device.PM10_value + "</td><td>" +  timeDiff + "</td></tr>";;
            });

            /* Old: Location,  Sensor, 2.5, 10, last update */
            /* Current: Location, 2.5, 10, last update */
            return htmlString;
        }
        
        var getSensorDataTableRows = function() {
            var returnArray = [];
            var tmpDevices = {};
            var delDevices = [];

            $.each( _devices, function( key, device ) {
                tmpDevices[key] = {};
                tmpDevices[key].id = key;
                tmpDevices[key].location = device.location.name;
            });

            $.each( _sensors, function( key, sensor ) {
                if( _sensorInfos[sensor.id].last_value == null )
                    return "";
                
                if( sensor.id.search(/test/i) >= 0 )
                    return "";
                
                if( sensor.sensor_type == 10 ) {
                    tmpDevices[sensor.parent_device]["PM10_id"] = sensor.id;
                    tmpDevices[sensor.parent_device]["PM10_value"] = Friskby.tools.round(_sensorInfos[sensor.id].last_value, 2);
                    tmpDevices[sensor.parent_device]["PM10_time"] = _sensorInfos[sensor.id].last_timestamp;
                }
                else if( sensor.sensor_type == 11 ) {
                    tmpDevices[sensor.parent_device]["PM25_id"] = sensor.id;
                    tmpDevices[sensor.parent_device]["PM25_value"] = Friskby.tools.round(_sensorInfos[sensor.id].last_value, 2);
                    tmpDevices[sensor.parent_device]["PM25_time"] = _sensorInfos[sensor.id].last_timestamp;
                }
            });

            $.each( tmpDevices, function( key, device ) {
               if( !device.hasOwnProperty("PM10_id") && !device.hasOwnProperty("PM25_id") )
                   delDevices.push(key);
            });

            $.each( delDevices, function( index, device ) {
                delete tmpDevices[device];       
            });

            $.each( tmpDevices, function( key, device ) {
                var timeDiff = Friskby.tools.timeDiffToHumanString(new Date( device.PM10_time ), new Date());
                if( device.PM10_time == null )
                    timeDiff = "-";
                var index = returnArray.length;
                returnArray[index] = [];
                returnArray[index][0] = "<a href='#' data-toggle='tooltip' data-placement='left' title='" + device.id + "'>" + device.location + "</a>";
                returnArray[index][1] = device.PM25_value;
                returnArray[index][2] = device.PM10_value;
                returnArray[index][3] = timeDiff;
            });
            return returnArray;
        }

        /**
         * Getters and setters
         **/
        var addSensor = function( newSensor ) {
            if( !newSensor.hasOwnProperty("id") )
                return false
            if( _sensors.hasOwnProperty( newSensor.id ))
                return false;

            _sensors[newSensor.id] = newSensor;
        }

        var addByArray = function( data, type ) {
            $.each( data, function( index, value ) {
                Friskby.tools.runFunction( "model", "add" + Friskby.tools.capitalizeFirstLetter( type ), value );
            });
        }

        var getSensor = function( sensorId ) {
            if( !_sensors.hasOwnProperty( sensorId ))
                return false;

            return _sensors[sensorId];
        }

        var addSensorInfo = function( newSensorInfo ) {
            if( !newSensorInfo.hasOwnProperty("id") )
                return false
            if( _sensorInfos.hasOwnProperty( newSensorInfo.id ))
                return false;

            _sensorInfos[newSensorInfo.id] = newSensorInfo;
        }

        var addSensorInfos = function( newSensorInfos ) {
            $.each( newSensorInfoss, function( index, value ) {
                addSensorInfo( value ); 
            });
        }

        var getSensorInfo = function( sensorId ) {
            if( !_sensorInfos.hasOwnProperty( sensorId ))
                return false;

            return _sensorInfos[sensorId];
        }

        var addSensorType = function( newSensorType ) {
            if( !newSensorType.hasOwnProperty( "id" ))
                return false

            _sensorTypes[newSensorType.id] = newSensorType;
        }

        var getSensorType = function( sensorTypeId ) {
            if( !_sensorTypes.hasOwnProperty( sensorTypeId ))
                return false;

            return _sensorTypes[sensorTypeId];
        }

        var addDevice = function( newDevice ) {
            if( !newDevice.hasOwnProperty("id") )
                return false;
            if( _devices.hasOwnProperty(newDevice.id) )
                return false;

            _devices[newDevice.id] = newDevice;
        }

        var getDevice = function( deviceId ) {
            if( !_devices.hasOwnProperty( deviceId ))
                return false;

            return _devices[deviceId];
        }

        var addLocation = function( newLocation ) {
            if( !newLocation.hasOwnProperty("id") )
                return false
            if( _locations.hasOwnProperty( newLocation.id ))
                return false;

            _locations[newLocation.id] = newLocation;
        }

        var getLocation = function( locationId ) {
            if( !_locations.hasOwnProperty( locationId ))
                return false;

            return _locations[locationId];
        }

        var addMeasurementType = function( newMeasurementType ) {
            if( !newMeasurementType.hasOwnProperty("id") )
                return false;
            if( _measurementTypes.hasOwnProperty( newMeasurementType.id ))
                return false;

            _measurementTypes.measurementType = newMeasurementType;
        }

        var getMeasurementTypeName = function( measurementTypeId ) {
            if( !measurementTypeId.hasOwnProperty( measurementTypeId ))
                return false;

            return _measurementType[measurementTypeId];
        }

        var getSensorLocation = function( sensorId ) {
            if( !_sensors.hasOwnProperty( sensorId ))
                return false;

            return _devices[_sensors[sensorId].parentDevice].location;
        }

        var getSensorSensorType = function ( sensorId ) {
            if( !_sensors.hasOwnProperty( sensorId ))
                return false;

            return _sensorTypes[_sensors[sensorId].sensor_type];
        }

        var getSensorMeasurementType = function( sensorId ) {
            if( !_sensors.hasOwnProperty( sensorId ))
                return false;

            return _measurementTypes[getSensorSensorType( sensorId ).measurement_type];
        }
        
        var getMeasurementTypeId = function ( sensorId ) {
            if( !_sensors.hasOwnProperty( sensorId ))
                return false;
            
            return getSensorSensorType( sensorId ).measurement_type;
        }

        var addTimeserie = function ( sensorId, timeserie ) {
            var measurementTypeId = getMeasurementTypeId( sensorId );
            
            if( !_timeSeries.hasOwnProperty( measurementTypeId ))
                _timeSeries[measurementTypeId] = {};
            
            if( timeserie.length == 0 ) {
                _timeSeries[measurementTypeId][sensorId] = timeserie;
                return;
            }
            
            var max = 0;
            var currentDate = new Date(timeserie[0][0])
            currentDate.setMinutes(0);
            currentDate.setSeconds(0);
            currentDate.setMilliseconds(0);
            var newDate;
            var timeserieMax = [];
            $.each( timeserie, function( index, sample ) {
                newDate = new Date(sample[0]);
                if( currentDate.getHours() == newDate.getHours() )
                    max = sample[1] > max ? sample[1] : max;
                else {
                    timeserieMax[timeserieMax.length] = [currentDate.toISOString(), max];
                    if( _getLocation( sensorId )[1] > 1 )
                        _addFeature( sensorId, _getLocation( sensorId ), max, currentDate.toISOString(), _getMeasurementTypeId( sensorId ));
                    max = sample[1];
                    _setBeginTime( currentDate );
                    currentDate = new Date(sample[0]);
                    currentDate.setMinutes(0);
                    currentDate.setSeconds(0);
                    currentDate.setMilliseconds(0);
                }
            });
            
            timeserieMax[timeserieMax.length] = [currentDate.toISOString(), max];
            if( _getLocation( sensorId )[1] > 1 )
                _addFeature( sensorId, _getLocation( sensorId ), max, currentDate.toISOString(), _getMeasurementTypeId( sensorId ));
            _setEndTime( currentDate );
            _timeSeries[measurementTypeId][sensorId] = timeserieMax;
        }
        
        var _setBeginTime = function( beginTime ) {
            try {
                if( beginTime < _beginTime || _beginTime === undefined )
                    _beginTime = beginTime;    
            }
            catch(error) {
                _beginTime = beginTime;
            }
        }
        
        var _setEndTime = function( endTime ) {
            try {
                if( endTime > _endTime || _endTime === undefined )
                    _endTime = endTime;
            }
            catch ( error ) {
                _endTime = endTime;
            }
        }
        
        var getBeginTime = function () {
            return _beginTime;
        }
        
        var getEndTime = function () {
            return _endTime;
        }
        
        var _getMeasurementTypeId = function ( sensorId ) {
            return _sensorInfos[sensorId].sensor_type.measurement_type.id;
        }

        var getTimeserie = function ( sensorId, measurementTypeId ) {
            if( !_timeSeries.hasOwnProperty( measurementTypeId ))
                return false;
            
            if( !_timeSeries[measurementTypeId].hasOwnProperty( sensorId ))
                return false;

            return _timeSeries[measurementTypeId][sensorId];
        }

        var getTimeseries = function () {
            return _timeSeries;
        }
        
        var _addFeatureCollection = function ( time, measurementTypeId ) {
            if( !_timeSeriesGeoJSON.hasOwnProperty ( measurementTypeId ))
                _timeSeriesGeoJSON[measurementTypeId] = {};
            if( !_timeSeriesGeoJSON[measurementTypeId].hasOwnProperty ( time )) {
                _timeSeriesGeoJSON[measurementTypeId][time] = {};
                _timeSeriesGeoJSON[measurementTypeId][time].type = "FeatureCollection";
                _timeSeriesGeoJSON[measurementTypeId][time].features = [];
            }    
        }
        
        var _addFeature = function ( sensorId, location, value, time, measurementTypeId ) {
            _addFeatureCollection( time, measurementTypeId );
            _timeSeriesGeoJSON[measurementTypeId][time].features.push( _createFeature( sensorId, location, value, time ));
        }
        
        var _createFeature = function ( sensorId, location, value, time ) {
            var feature = {};
            feature.type = "Feature";
            feature.geometry = {};
            feature.geometry["type"] = "Point";
            feature.geometry["coordinates"] = location;
            feature.properties = {};
            feature.properties.state = value > 0 ? value > 35 ? "BreakingThreshold" : "WithinThreshold" : "Inactive";
            feature.properties.value = value;
            feature.properties.time = time;
            feature.properties.sensorId = sensorId;
            return feature;
        }
        
        var _getLocation = function ( sensorId ) {
            return [_sensorInfos[sensorId].parent_device.location.longitude, _sensorInfos[sensorId].parent_device.location.latitude];
        }

        var getTimeSeriesGeoJSON = function () {
            return _timeSeriesGeoJSON;
        }
        return {
            apiUrl: apiUrl,
            apiUrlArray: apiUrlArray,
            apiUrlTimeseriesArray: apiUrlTimeseriesArray,
            apiUrlTimeserie: apiUrlTimeserie,
            getInfoHTML: getInfoHTML,
            getSensorTableRows: getSensorTableRows, 
            getSensorDataTableRows: getSensorDataTableRows, 
            addByArray: addByArray,
            addSensor: addSensor,
            getSensor: getSensor,
            addSensorType: addSensorType,
            getSensorType: getSensorType,
            addSensorInfo: addSensorInfo,
            getSensorInfo: getSensorInfo,
            addDevice: addDevice,
            getDevice: getDevice,
            addLocation: addLocation,
            getLocation: getLocation,
            addMeasurementType: addMeasurementType,
            getMeasurementType: getMeasurementTypeName,
            addTimeserie: addTimeserie,
            getTimeserie: getTimeserie,
            getTimeseries: getTimeseries,
            sensors: _sensors,
            sensorTypes: _sensorTypes,
            devices: _devices,
            locations: _locations,
            measurementTypes: _measurementTypes,
            sensorInfo: _sensorInfos,
            getBeginTime: getBeginTime,
            getEndTime: getEndTime,
            getTimeSeriesGeoJSON: getTimeSeriesGeoJSON
        }
    })();


    Friskby.controller = (function () {
        var _selectedSensor; /* sensor ID */
        var _isPlaying = false;
        var _timelineStart;
        var _timelineEnd;
        var _timelineSpeed;
        var _model;
        var _map;
        var _chart;
        var _activeLayer = {measurementTypeId: null, time: null};
        var _slider;

        var _getView = function () {

        }

        var _getOLMap = function () {

        }

        var _getSensorInfo = function () {

        }

        var _getChart = function () {

        }

        var setModel = function( model ) {
            _model = model;
        }

        var setMap = function ( map ) {
            _map = map;
        }

        var setChart = function ( chart ) {
            _chart = chart;
        }

        var _initModel = function() {
            /* TODO
            onload the page
            ajax all the data into the model
            */
        }

        var _getTimeline = function( start, end ) {
            /* TODO
             * create one vector layer for each time, and then change the view for each timestamp?
             */
        }

        var sensorSelect = function ( sensorId ) {
            selectedSensor = _model.getSensor(sensorId);
            /* TODO
             * Set chart
             * Set sensor info
             * etc..
             */
        }

        var playTimeline = function ( ) {
            /* TOOD */
        }

        var changePlaySpeed = function ( speed ) {
            /* TODO */
        }

        var populateModel = function( ) {

            $("#progress").html("<i class='fa fa-spinner fa-pulse fa-3x fa-fw'></i><span class='sr-only'>Loading...</span>");

            var modelApi = _model.apiUrlArray();
            var modelRequests = modelApi.urls.map( function( url ) {
                return $.getJSON( url );
            });

            $.when.apply($, modelRequests).then( function () {
                $.each( arguments, function( index, value ) {
                    // 0: data, 1: text status, 2: jqXHR
                    if( value[1] == "success" ) 
                        _model.addByArray( value[0], modelApi.keys[index] );
                    else {
                        console.log("Something went wrong loading JSON.. ");
                        console.log(value[0]);
                        console.log(value[1]);
                        console.log(value[2]);
                    }        
                });
                return [].slice.call(arguments);
            }).fail( function( a ) {
                /* TODO failed */
            }).done( function( a ) {
                var timeseriesApi = _model.apiUrlTimeseriesArray( [10, 11] );
                var timeseriesRequests = timeseriesApi.urls.map( function( url ) {
                    return $.getJSON( url );
                });

                 $.when.apply($, timeseriesRequests ).then( function () {
                    $.each( arguments, function( index, value ) {
                        // 0: data, 1: text status, 2: jqXHR
                        if( value[1] == "success" ) {
                            var sensorId = timeseriesApi.keys[index];
                            if( sensorId.indexOf(/test/i) < 0 )
                                _model.addTimeserie( timeseriesApi.keys[index], value[0] );
                        }
                        else {
                            console.log("Something went wrong loading JSON.. ");
                            console.log(value[0]);
                            console.log(value[1]);
                            console.log(value[2]);
                        }        
                    });
                    return [].slice.call(arguments);
                }).fail( function( a ) {
                    /* TODO failed */
                }).done( function( a ) {
                    console.log("Done! Refreshing GUI..");
                    $("#progress").html("");
                    refresh();
                    setUpGui();
                });
            });
        }

        var _highchartsDataObject = function( name, inData ) {
            var tempData = [];

            $.each( inData, function( sensorId, values ) {
                var tempDate = new Date(values[0]).getTime();
               /*tempData.push( [new Date(values[0]), values[1]] ); */
               tempData.push( [tempDate, values[1]] ); 
            });

            return {
                name: name,
                data: tempData
            }    
        }

        var _populateChartSeries = function () {
            $.each( _model.getTimeseries(), function( measurementTypeId, timeseries ) {
                $.each( timeseries, function( sensorId, timeserie ) {
                    /*if( _model.getSensorInfo( sensorId ).last_value == null )
                        return true;*/
                    if( timeserie.length > 0 )
                        _chart.addTimeserie( _highchartsDataObject( _model.getSensorInfo(sensorId).parent_device.location.name, timeserie ), measurementTypeId );        
                });
            });
        }

        var refresh = function() {
            $('#sensor-table').DataTable({
                data: _model.getSensorDataTableRows(),
                "scrollY":          "300px",
                "scrollCollapse":   true,
                "paging":           false,
                "info":             false,
                "searching":        false
                
            } );
            
            $("#info-sensor-info").html( _model.getInfoHTML("FriskPI06_PM10"));
            
            $("#progress").html("");
            
            $.each( _model.getTimeSeriesGeoJSON(), function( measurementTypeId, timeserie ) {
                $.each( timeserie, function( time, geoJSON ) {
                   _map.addGeoJSONLayer( geoJSON, {"measurementTypeId": measurementTypeId, "time": time} );  
                });
            });
            
            _activeLayer.measurementTypeId = 8;
            _activeLayer.time = _model.getEndTime().toISOString();
            _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
            $("#timeBox").html(Friskby.tools.timeString(new Date(_activeLayer.time)));
            
            _populateChartSeries();
            _chart.plot("sensor-chart-all");
            _chart.setCategory( _activeLayer.measurementTypeId );
        }

        var setUpGui = function() {
            /* Set up layer control */
            
            $('#pm25Button').on('click', function (e) {
                _activeLayer.measurementTypeId = 9;
                _chart.setCategory( _activeLayer.measurementTypeId );
                _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
                $('#pm25Button').addClass( "active" );
                $('#pm10Button').removeClass( "active" );
            });
            
            $('#pm10Button').on('click', function (e) {
                _activeLayer.measurementTypeId = 8;
                _chart.setCategory( _activeLayer.measurementTypeId );
                _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
                $('#pm10Button').addClass( "active" );
                $('#pm25Button').removeClass( "active" );
            });
            
            _slider = $("#friskTimeslider").slider({
                max: _model.getEndTime().getTime(),
                min: _model.getBeginTime().getTime(),
                step: 1000*60*60,
                value: _model.getEndTime().getTime(),
                change: function( event, ui ) {
                    var time = new Date( ui.value );
                    _activeLayer.time = time.toISOString();
                    _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
                    _chart.markTime( time );
                    $("#timeBox").html(Friskby.tools.timeString(new Date(time)));
                },
                slide: function( event, ui ) {
                    var time = new Date( ui.value );
                    _activeLayer.time = time.toISOString();
                    _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
                    _chart.markTime( time );
                    $("#timeBox").html(Friskby.tools.timeString(new Date(time)));
                },
                stop: function( event, ui ) {
                    var time = new Date( ui.value );
                    _activeLayer.time = time.toISOString();
                    _map.viewLayer( _activeLayer.measurementTypeId, _activeLayer.time );
                    _chart.markTime( time );
                     //$("#timeBox").html(new Date(time).toDateString()); 
                }
            });
            
            $('#timelinePlayButton').on('click', function (e) {
                _timelinePlay();
                $('#timelinePlayButton').addClass( "active" );
                console.log("Supposed to play now..");
                
            });
            
            $('#timelinePauseButton').on('click', function (e) {
                _timelinePause();
                $('#timelinePlayButton').removeClass( "active" );
            });
            
            $(function () {
              $('[data-toggle="tooltip"]').tooltip()
            });
        }
        
        var _timeoutID;

        var _timelinePlay = function () {
            if( !_isPlaying ) {
                _isPlaying = true;
                _timeoutID = window.setTimeout(_timelineNext, 1000);
                console.log("Starting to play timeline");
            }
        }

        var _timelinePause = function () {
            if( _isPlaying )
                window.clearTimeout(_timeoutID);
            
            _isPlaying = false;
        }
        
        var _timelineNext = function () {
            var friskTimeslider = $( "#friskTimeslider" );
            if( friskTimeslider.slider("value") == friskTimeslider.slider("option").max )
                friskTimeslider.slider("value", friskTimeslider.slider("option").min );
            else
                friskTimeslider.slider("value", friskTimeslider.slider("value") + friskTimeslider.slider("option").step );
            
            _timeoutID = window.setTimeout(_timelineNext, 1000);
        }
        
        return {
            populateModel: populateModel,
            sensorSelect: sensorSelect,
            playTimeline: playTimeline,
            changePlaySpeed: changePlaySpeed,
            refresh: refresh,
            setModel: setModel,
            setMap: setMap,
            setChart: setChart,
            setUpGui: setUpGui,

            /*
            L.geoJson( Friskby.model.getSensorGeoJSON( 8 ).geoJSON ).addTo( Friskby.leaflet.map );
            L.geoJson( Friskby.model.getSensorGeoJSON( 9 ).geoJSON ).addTo( Friskby.leaflet.map );
            */
        }
    })();

    /**
     * Require OpenLayers 3
     *
     **/
    Friskby.olMap = (function () {
        /* The open layers map object */
        var _map;
        /* the DOM element to use - default = map */
        var _domElement;
        /* Datum WGS84, UTM zone 33N */
        var _UTM33 = 'EPSG:32633';
        /* WGS84 */
        var _WGS84 = 'EPSG:4326';
        /* The WMTS source from Kartverket use UTM33 */
        var _srcProjection = _UTM33;

        /* Set the location of the proj4 library */
        ol.proj.setProj4(proj4);

        /* Define the UTM33 for Proj4js */
        proj4.defs([
            [
                'EPSG:32633',
                '+proj=utm +zone=33 +datum=WGS84 +units=m +no_defs'
            ]
        ]);

        /* Configure Open Layers for the Kartverket map. Reference: http://kartverket.no/Kart/Gratis-kartdata/WMS-tjenester/ */
        var _projection =  ol.proj.get(_srcProjection);
        var _projectionExtent = [-2500000, 3500000, 3045984, 9045984];
        var _resolutions = [21664, 10832, 5416, 2708, 1354, 677, 338.5, 169.25, 84.625, 42.3125, 21.15625, 10.578125, 5.2890625, 2.64453125, 1.322265625, 0.6611328125, 0.33056640625, 0.165283203125];
        var _matrixIds = [];
        for (var z = 0; z < 18; ++z) {
            /**
             * Max 18? .. eller 21? 
             * generate resolutions and matrixIds arrays for this WMTS
             * resolutions[z] = size / Math.pow(2, z);
             *
             */
            _matrixIds[z] = _srcProjection + ":" + z;
        }

        /**
         * Sensor types = array with Integer sensor types
         viewLa
         */
        var addGeoJSONLayer = function ( geoJSON, keyValuePairs ) {
            var vectorSource = new ol.source.Vector({
                features: (new ol.format.GeoJSON()).readFeatures( geoJSON, {dataProjection: 'EPSG:4326', featureProjection: 'EPSG:32633'})
            });

            var vectorLayer = new ol.layer.Vector({ source: vectorSource, style: _styleFunction});
            $.each( keyValuePairs, function( key, value ) {
                vectorLayer.set(key, value, true );    
            });
            _map.addLayer(vectorLayer);
        }

        var viewLayer = function( measurementTypeId, time ) {
            _map.getLayers().forEach( function( layer, index, array ) {
                if( layer.get("measurementTypeId") == measurementTypeId && layer.get("time") == time ) {
                    layer.setVisible( true );
                    _map.getView().fit( layer.getSource().getExtent(), _map.getSize() );    
                }
                else if( $.inArray( "measurementTypeId", layer.getKeys() ) >= 0 )
                    layer.setVisible( false );
            });
            // _map.getView().setProperties({extent: _map.getView().calculateExtent( _map.getSize())});
        }

        /**
         *
         * Configure the Open Layers map
         *
         */
        var load = function( domElement ) { 
            _domElement = domElement;
            _map = new ol.Map({
                target: _domElement,
                controls: ol.control.defaults({
                        attributionOptions: /** @type {olx.control.AttributionOptions} */ ({
                            collapsible: false
                        })
                    })/*.extend(
                        [new ol.control.ZoomToExtent({target: document.getElementById('map')})]
                    )*/,
                layers: [
                    /* Define the Kartverket map layer */
                    new ol.layer.Tile({
                        title: "Norway",
                        source: new ol.source.WMTS({
                            url: "http://opencache.statkart.no/gatekeeper/gk/gk.open_wmts?",
                            layer: 'norges_grunnkart_graatone',
                            matrixSet: 'EPSG:32633',
                            format: 'image/png',
                            projection: _projection,
                            tileGrid: new ol.tilegrid.WMTS({
                                extent: _projectionExtent,
                                resolutions: _resolutions,
                                matrixIds: _matrixIds
                            })
                        })
                    })],
                view: new ol.View({
                    projection: _srcProjection,
                    center: [-33475.34364682839,6732061.012181105],
                    zoom: 9,
                    minZoom: 9,
                    maxZoom: 17
                })
            });
        }

        /**
         *
         *  Sensor styles
         *
         */
        var _circleGray = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 5,
                fill: new ol.style.Fill({color: 'rgba(155,155,155,0.4)'}),
                stroke: new ol.style.Stroke({color: 'black', width: 3})
            }),
            text: new ol.style.Text({
                font: '10px Calibri,sans-serif',
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        });

        var _circleGreen = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 15,
                fill: new ol.style.Fill({color: 'rgba(55,255,55,0.4)'}),
                stroke: new ol.style.Stroke({color: 'green', width: 3})
            }),
            text: new ol.style.Text({
                font: '10px Calibri,sans-serif',
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        });

        var _circleRed = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 15,
                fill: new ol.style.Fill({color: 'rgba(255,55,55,0.4)'}),
                stroke: new ol.style.Stroke({color: 'red', width: 3})
            }),
            text: new ol.style.Text({
                font: '10px Calibri,sans-serif',
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        });

        var _circleSelected = new ol.style.Style({
            image: new ol.style.Circle({
                radius: 18,
                fill: new ol.style.Fill({color: 'rgba(200,150,40,0.6)'}),
                stroke: new ol.style.Stroke({color: 'orange', width: 1})
            }),
            text: new ol.style.Text({
                font: '12px Calibri,sans-serif',
                fill: new ol.style.Fill({
                    color: '#000'
                }),
                stroke: new ol.style.Stroke({
                    color: '#fff',
                    width: 3
                })
            })
        });

        var _stylesToStateMapping = {
          'Inactive': _circleGray,
          'BreakingThreshold': _circleRed,
          'WithinThreshold': _circleGreen
        };

        var _styleFunction = function(feature, resolution) {
            switch( feature.getProperties().state ) {
                case 'BreakingThreshold':
                case 'WithinThreshold':
                    //styles[feature.getProperties().state].getText().setText(resolution < 5000 ? feature.getProperties().last_value : '');
                    _stylesToStateMapping[feature.getProperties().state].getText().setText("" + feature.getProperties().value);
                    break;
                default:
                    break;
            }
            return _stylesToStateMapping[feature.getProperties().state];
        };

        var getMap = function() {
            return _map;
        }
        return {
            map: getMap,
            load: load,
            viewLayer: viewLayer,
            addGeoJSONLayer: addGeoJSONLayer
        }
    })();

    Friskby.highcharts = (function () {
        var _series = {};
        var _chart;
        var _category;
        
        var addTimeserie = function( timeserie, category ) {
            if( !_series.hasOwnProperty( category ))
                _series[category] = [];
            
            _series[category].push( timeserie );
        }
        
        var setCategory = function( category ) {
            if( _series.hasOwnProperty( category )) {
                while(_chart.series.length > 0)
                    _chart.series[0].remove(true);
                
                _category = category;
                $.each(_series[_category], function(index, serie) {
                    _chart.addSeries( serie );    
                });
            }
        }
        
        var markTime = function( time ) {
            _chart.xAxis[0].removePlotBand('Chosen time');

            _chart.xAxis[0].addPlotLine({
				value: time,
				color: 'rgb(0, 0, 0)',
				width: 3,
				id: 'Chosen time'
			});
        }

        var plot = function( domElement ) {
            
            Highcharts.setOptions({
                global: {
                    timezoneOffset: new Date().getTimezoneOffset()
                }
            });

            
            _chart = new Highcharts.Chart({
                chart: {
                    renderTo: domElement,
                    type: 'line',
                    backgroundColor: 'transparent',
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
                    min: 0/*,
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
                series: [{
                    name: 'Dummy',
                    data: [0.0],
                    color: '#F33'
                }]
            });
        }
        
        var getChart = function() {
            return _chart;
        }
        
        var getCategory = function() {
            return _category;
        }
        
        var getSeries = function() {
            return _series;   
        }
        
        return {
            addTimeserie: addTimeserie,
            plot: plot,
            markTime: markTime,
            chart: getChart,
            setCategory: setCategory,
            category: getCategory,
            series: getSeries
        }
    })();

    Friskby.tools = (function () {
        
        var timeDiffToHumanString = function( fromDate, toDate ) {
            var sizes = {
                now: {
                    minSize: 0,
                    maxSize: 1000*60*10,
                    string: function( time ) {return "now";}
                },
                lessThanAnHour: {
                    minSize: 1000*60*10,
                    maxSize: 1000*60*60,
                    string: function( time ) {return "less than an hour";}
                },
                moreThanHour: {
                    minSize: 1000*60*60,
                    maxSize: 1000*60*60*24,
                    string: function( time ) {
                        return "> " + Math.round(time/(1000*60*60)) + " hours";
                    }
                },
                moreThanDay: {
                    minSize: 1000*60*60*24,
                    maxSize: 1000*60*60*24*7,
                    string: function( time ) {
                        return "> " + Math.round(time/(1000*60*60*24)) + " days";
                    }
                },
                moreThanWeek: {
                    minSize: 1000*60*60*24*7,
                    maxSize: 1000*60*60*24*30,
                    string: function( time ) {
                        return "> " + Math.round(time/(1000*60*60*24*7)) + " weeks";
                    }
                },
                moreThanMonth: {
                    minSize: 1000*60*60*24*30,
                    maxSize: 1000*60*60*24*45,
                    string: function( time ) {return " > a month";}
                },
                alongWhile: {
                    minSize: 1000*60*60*24*45,
                    maxSize: 1000*60*60*24*365*100,
                    string: function( time ) {return " > a month";}
                }
            }
            
            diff = toDate - fromDate;
            
            var returnString = "unknown";
            $.each( sizes, function( index, size ) {
                if( diff <= size.maxSize && diff >= size.minSize ) {
                    returnString = size.string( diff );
                    return false;
                }
            });
            
            return returnString;
        }
        
        var timeDiffToString = function( fromDate, toDate ) {     
            var diff, temp;
            var sizes = ["year", "month", "day", "hour", "minute", "second"];
            var string = "";

            var unit = {
                second: "s",
                minute: "m",
                hour: "h",
                day: "d",
                month: "months",
                year: "y"
            }

            var result = {
                second: 0,
                minute: 0,
                hour:   0,
                day:    0,
                month:  0,
                year:   0
            }

            var size = {
                second: 1000,
                minute: 1000*60,
                hour:   1000*60*60,
                day:    1000*60*60*24,
                month:  1000*60*60*24*30,
                year:   1000*60*60*24*365
            };

            diff = toDate - fromDate;
            var offset = new Date().getTimezoneOffset();
            
            offset = offset * size.minute;
        
            diff += offset;
            
            $.each( sizes, function( i, s) {
                debug( "\tSize " + s +":")
                if( diff > size[s] ) {
                    debug( "\t\tDiff " + diff + " > size " + size[s] + ":", false);
                    temp = diff / size[s];
                    result[s] = Math.floor(temp);
                    diff = (temp-result[s]) * size[s];
                    string += result[s] + " " + unit[s] + ", ";
                }
            });

            string = string.substr(0, string.length - 2);
            
            return string;
        };
        
        var timeString = function ( date ) {
            var weekDay = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
            return weekDay[date.getDay()] + " " + (date.getHours()<10?"0":"") + date.getHours() + ":" + (date.getMinutes()<10?"0":"") + date.getMinutes();
        }

        var runFunction = function(module, name, arguments) {
            var fn = Friskby[module][name];
            if(typeof fn !== 'function')
                return;

            fn.apply(window, [arguments]);
        }

        var capitalizeFirstLetter = function (string) {
            return string.charAt(0).toUpperCase() + string.slice(1);
        }
        
        var round = function(value, decimals) {
            return Number(Math.round(value+'e'+decimals)+'e-'+decimals);
        }
        
        var debug = function( string, debugOff ) {
            if( debugOff ) return;
            
            console.log( string );
        }


        return {
            timeDiffToString: timeDiffToString,
            timeDiffToHumanString: timeDiffToHumanString,
            capitalizeFirstLetter: capitalizeFirstLetter,
            runFunction: runFunction,
            timeString: timeString,
            round: round,
            debug: debug
        }
    })();
    
    return Friskby;

}) ( Friskby || {} );