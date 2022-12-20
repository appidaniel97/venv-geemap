#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Installs geemap package
import subprocess
import webbrowser

try:
    import geemap
except ImportError:
    print('geemap package not installed. Installing ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', '-U', 'geemap'])

# In[2]:


import ee
import geemap

# In[10]:


Map = geemap.Map(center=[40, -100], zoom=4)
Map.add_basemap('HYBRID')  # Add Google Satellite
Map

# In[8]:


image = (
    ee.ImageCollection('MODIS/MCD43A4_006_NDVI')
    .filter(ee.Filter.date('2018-04-01', '2018-05-01'))
    .select("NDVI")
    .first()
)

vis_params = {
    'min': 0.0,
    'max': 1.0,
    'palette': [
        'FFFFFF',
        'CE7E45',
        'DF923D',
        'F1B555',
        'FCD163',
        '99B718',
        '74A901',
        '66A000',
        '529400',
        '3E8601',
        '207401',
        '056201',
        '004C00',
        '023B01',
        '012E01',
        '011D01',
        '011301',
    ],
}
Map.setCenter(-7.03125, 31.0529339857, 2)
# Map.addLayer(image, vis_params, 'MODIS NDVI')

countries = ee.FeatureCollection('users/giswqs/public/countries')
style = {"color": "00000088", "width": 1, "fillColor": "00000000"}
# Map.addLayer(countries.style(**style), {}, "Countries")

ndvi = image.visualize(**vis_params)
blend = ndvi.blend(countries.style(**style))

# Map.addLayer(blend, {}, "Blend")

Map

# In[9]:


import ipywidgets as widgets
from ipyleaflet import WidgetControl
from geemap import geojson_to_ee

# Get basemap layers
base_layers = Map.layers

feat_list = []
# Get the DrawControl
dc = Map.draw_control


# Handle draw events
def handle_draw(self, action, geo_json):
    geom = geojson_to_ee(geo_json, False)
    feature = ee.Feature(geom)
    feat_list.append(feature)
    collection = ee.FeatureCollection(feat_list)
    clip_image = image.clipToCollection(collection)

    Map.layers = base_layers[:3]
    Map.addLayer(clip_image, vis_params, 'SRTM DEM')
    # Map.addLayer(ndvi, ndviParams, 'NDVI image')

    #     Map.addLayer(ee.Image().paint(collection, 0, 2), {'palette': 'red'}, 'EE Geometry')
    # Map.addLayer(collection, {}, 'Drawing Features')


dc.on_draw(handle_draw)

Map

Map.save("testmap.html")
webbrowser.open("testmap.html")
# In[ ]:




