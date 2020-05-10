import folium
import pandas

# use pandas to create a data frame that stores data from csv file
data = pandas.read_csv("Volcanoes.txt")

# list variables to store all the lat and long values
lat_lst = list(data["LAT"])
long_lst = list(data["LON"])
elev_lst = list(data["ELEV"])

# function determines colour of volcano marker based on elevation


def colour_group(elevation):
    if elevation < 1000:
        return "green"
    elif elevation < 2000:
        return "orange"
    elif elevation < 3000:
        return "blue"
    else:
        return "red"


# base-layer - street map
# we created a folium map object
map = folium.Map(location=[39.731, -104.951], zoom_start=4,
                 tiles="OpenStreetMap")

# for adding children to our map, use feature group
# this feature group consists of CircleMarker layer for volcanoes
fg_vol = folium.FeatureGroup(name="Volcanoes")

# marker is a feature, so you can add many features using feature group

# loop all items on both lists and add circle mark for each volcano
for lat, long, elev in zip(lat_lst, long_lst, elev_lst):

    fg_vol.add_child(folium.CircleMarker(
        location=[lat, long], radius=10, popup=str(elev) + " m", fill_color=colour_group(elev), color="grey", fill_opacity="0.7"))

# this feature group consists of GeoJson layer for population
fg_pop = folium.FeatureGroup(name="Population")

# polygon layer used to distinguish each country
# colour coded based on population

fg_pop.add_child(folium.GeoJson(
    data=open("world.json", "r", encoding="utf-8-sig").read(),
    style_function=lambda x: {"fillColor": "green" if x["properties"]["POP2005"] < 50000000
                              else "orange" if 50000000 <= x["properties"]["POP2005"] < 100000000
                              else "yellow" if 100000000 <= x["properties"]["POP2005"] < 20000000
                              else "red"}))


# this helps organize all the children
map.add_child(fg_vol)
map.add_child(fg_pop)

# allows user to control the layers - toggle on and off
map.add_child(folium.LayerControl())

map.save("index.html")
