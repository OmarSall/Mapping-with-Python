import folium
import pandas as pd

data = pd.read_csv("Volcanoes.txt")
lat = list(data["LAT"])
lon = list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""


# fg.add_child(folium.Marker(location = [52.2,18.1], popup = "Hi I am a Marker", icon = folium.Icon(color = 'green')))

# for coordinates in [[52.2,18.1],[51.21,17.01]]:
#     fg.add_child(folium.Marker(location = coordinates, popup = "Hi I am a Marker", icon = folium.Icon(color = 'green')))

#popup = folium.Popup(str(el), parse_html = True) - to avoid a blank webpage due to the quotes

def color_producer(elevation):
    if elevation < 1000:
        return 'green'
    elif 1000 <= elevation < 3000:
        return 'orange'
    else:
        return 'red'


map = folium.Map(location=[51.21917,17.01442], zoom_start = 15, tiles = "Stamen Terrain")  # Mapbox Bright

fgv = folium.FeatureGroup(name = "Volcanoes")


for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.Marker(location = [lt,ln], popup = folium.Popup(str(el) + " meters", parse_html = True), icon = folium.Icon(color = color_producer(el))))

    fgv.add_child(folium.CircleMarker(location = [lt,ln], radius = 10, popup = str(el) + " m",
    fill_color = color_producer(el), color = 'black', fill_opacity = 0.6))

# RegularPolygonMarker(location, number_of_sides=4, rotation=0, radius=15, popup=None, tooltip=None, **kwargs)

fgp = folium.FeatureGroup(name = "Population")

fgp.add_child(folium.GeoJson(data=open('world.json','r', encoding = 'utf-8-sig').read(),
style_function = lambda x:{'fillColor':'green' if x['properties']['POP2005'] < 10000000 
else 'orange' if 100000000 <= x['properties']['POP2005'] < 20000000 else 'red'} ))


map.add_child(fgv)
map.add_child(fgp)

map.add_child(folium.LayerControl())

# map.save("Map1VS.html")

map.save("Map_html_popup_advanced.html")