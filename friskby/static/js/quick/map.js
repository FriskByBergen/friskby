function normalize(val, minIn, maxIn, maxOut) {
  var delta = (maxIn - minIn);
  var norm_val = val;
  norm_val = Math.min(Math.max(norm_val, minIn), maxIn) + delta;
  norm_val = (norm_val / delta) * maxOut;
  norm_val = Math.floor(norm_val);
  return norm_val;
}

function createmap() {
  var map = new ol.Map({
    target: 'map',
    layers: [
      new ol.layer.Tile({
        source: new ol.source.OSM()
      })
    ],
    view: new ol.View({
      center: ol.proj.fromLonLat([5.3349616, 60.3940185]),
      zoom: 11
    })
  });
  var styleFunc = function(list, timestamp) {
    return function(feature, resolution) {
      var data = feature.getProperties()["sensor"][list];
      if (data.length == 0 || data[data.length - 1] == undefined)
        return new ol.style.Style({visible: false});

      var val = data[data.length - 1].value;
      var norm_val = normalize(val,-20, 20,255);
      var color = 'rgba(' + norm_val + ',' + (255 - norm_val) + ',0,1)';
      return new ol.style.Style({
        fill: new ol.style.Fill({color: color}),
        stroke: new ol.style.Stroke({color: 'white', width: 3}),
        text: new ol.style.Text({
            font: '10px Calibri,sans-serif',
            fill: new ol.style.Fill({
                color: '#000'
            }),
            stroke: new ol.style.Stroke({
                color: '#fff',
                width: 3
            }),
            text: "" + val.toFixed(1)
        })
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
