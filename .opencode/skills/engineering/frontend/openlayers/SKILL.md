---
name: openlayers
description: OpenLayers Map, View, VectorLayer, VectorSource, and interactions for web maps. Use when working on map features in the the-frontend-portal (the-frontend-portal)-AOI, vessels, layers, draw, or geo-visualization in the the-project Platform ecosystem.
---

# OpenLayers - the-frontend-portal

Skill for **OpenLayers** in the the-frontend-portal project (geospatial visualization, areas of interest, vessels). Reference documentation: [OpenLayers](https://openlayers.org/).

## Technology Stack (the-frontend-portal)

- **OpenLayers:** 6.10.0 (the-frontend-portal the-frontend-portal)
- **Proj4:** 2.9.2 (cartographic projections)
- **Project:** `the-frontend-portal/the-frontend-portal/`

## When to Use This Skill

- Add or configure layers (vector, tile)
- Draw or edit geometries (AOI, polygons)
- Show vessel positions or surveillance zones
- Integrate with shared map API (centerMapByVesselId, centerMapByAoiFeature, createAoi, etc.)

## Core Concepts

- **Map:** contains layers and view.
- **View:** center, zoom, projection.
- **Layer:** Tile (OSM, WMS) or Vector.
- **Layer:** Tile (OSM, WMS) or Vector.
- **VectorSource:** features (GeoJSON, points, polygons).
- **VectorLayer:** displays VectorSource with style.

## Map and Vector Layer

```javascript
import Map from 'ol/Map.js';
import View from 'ol/View.js';
import VectorLayer from 'ol/layer/Vector.js';
import VectorSource from 'ol/source/Vector.js';
import GeoJSON from 'ol/format/GeoJSON.js';

const vectorSource = new VectorSource({
  url: 'https://example.com/features.geojson',
  format: new GeoJSON(),
});

const vectorLayer = new VectorLayer({
  source: vectorSource,
  style: styleFunction, // (feature, resolution) => new Style({...})
});

const map = new Map({
  target: 'map',
  layers: [vectorLayer],
  view: new View({ center: [0, 0], zoom: 2 }),
});
```

## VectorSource

- **Features:** `addFeature`, `removeFeature`, `getFeatures()`, `getFeaturesInExtent(extent)`.
- **URL + format:** load GeoJSON/WFS.
- **Loader with bbox:** for large datasets (strategy: bbox, loader that requests by extent).
- **Events:** `addfeature`, `removefeature`, `featuresloadend`.

## Draw Interaction

- Add drawing (Point, LineString, Polygon, Circle) with `ol/interaction/Draw`.
- Draw source = VectorSource of the layer where features are stored.
- Events: `drawstart`, `drawend`, `drawabort`.

```javascript
import Draw from 'ol/interaction/Draw.js';

const draw = new Draw({ source: vectorSource, type: 'Polygon' });
map.addInteraction(draw);
draw.on('drawend', function (evt) {
  const feature = evt.feature;
  // get coordinates: feature.getGeometry().getCoordinates()
});
```

## the-frontend-portal Context

- Integration with shared API: `map.centerMapByVesselId`, `map.centerMapByAoiFeature`, `map.createAoi`, `map.enableAoiLayer`, etc.
- Projections: use proj4 when needed (units, CRS).
- Export KML: format supported by the the-frontend-portal for export.

## Best Practices

- Use per-feature style when appearance depends on properties (color, label).
- For many features, consider `declutter` or `renderMode: 'image'` when appropriate.

## Reference

- OpenLayers: https://openlayers.org/
- Context7 library ID: `/openlayers/openlayers`
