function normalize( val, minIn, maxIn, minOut, maxOut )  {
  var r = Math.max( Math.min( val, maxIn ), minIn) ;
  var deltaIn = maxIn - minIn;
  var deltaOut = maxOut - minOut;
  r = minOut + deltaOut * (r - minIn) / deltaIn;
  r = Math.floor(r);
  return r;
}

function createmap() {
  var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.Stamen({ 
          'toner-lite'
        })
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([5.335, 60.394]),
      zoom: 10
    })
  });
  var styleFunc = function(list, timestamp) {
    return function(feature, resolution) {
      var data = feature.getProperties()["sensor"][list];
      if (data.length == 0 || data[data.length - 1] == undefined)
        return new ol.style.Style({visible: false});

      var val = data[data.length - 1].value;
      var norm_val = normalize(val,0,35,0,255);
      var color = 'rgba(' + norm_val + ',' + (255 - norm_val) + ',0,1)';
      return new ol.style.Style({
        fill: new ol.style.Fill({color: color})
      });
    };
  };
  var vectorSource = new ol.source.Vector();
  values.forEach(function(value) {
    vectorSource.addFeature(
      new ol.Feature({
        "geometry" : new ol.geom.Circle(
          ol.proj.transform([value.long, value.lat], 'EPSG:4326', 'EPSG:3857'),
          1000),
        "sensor": value }));
  });

  var selectClick = new ol.interaction.Select({
    condition: ol.events.condition.click,
    multi: true
  });
  map.addInteraction(selectClick);
  selectClick.on('select', function(e) {
      console.log('click ' +
          e.target.getFeatures().getLength() +
          ' selected features (last operation selected ' + e.selected.length +
          ' and deselected ' + e.deselected.length + ' features)');
    });
  return {
    onSelect: function(callback) {
      selectClick.on('select', function(e) {
        e.selected.forEach(function(feature) {
          callback(feature.getProperties()["sensor"]["id"]);
        });
      });
    },
    showDataFor: function(sensors, key, timestamp) {
       map.getLayers().forEach(function(l) {
         if (l.get("name") === "layer") map.removeLayer(l);
      });
      var layer = new ol.layer.Vector({
        source: vectorSource,
        style: styleFunc(key, timestamp)
      });
      layer.set("name", "layer");
      map.addLayer(layer);
    }
  };
};
