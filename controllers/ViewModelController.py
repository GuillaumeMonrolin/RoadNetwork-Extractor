import os
from pathlib import Path

from geopy import Nominatim

from core.CanvaCreator import generate_canva
from core.OpenStreetMapService import Map

TMP_NETWORK_PATH = None
FINAL_SVG_PATH = None

CITY_NAME = ""
CITY_RADIUS = 0

NETWORK_FILTER = None

def generate_layer_filter(motorway, trunk, primary, secondary, tertiary):
    clean_layer_list = '["highway"~"'
    should_add_separator = False
    if motorway:
        if should_add_separator:
            clean_layer_list += '|'
        should_add_separator = True
        clean_layer_list += 'motorway'
    if trunk:
        if should_add_separator:
            clean_layer_list += '|'
        should_add_separator = True
        clean_layer_list += 'trunk'
    if primary:
        if should_add_separator:
            clean_layer_list += '|'
        should_add_separator = True
        clean_layer_list += 'primary'
    if secondary:
        if should_add_separator:
            clean_layer_list += '|'
        should_add_separator = True
        clean_layer_list += 'secondary'
    if tertiary:
        if should_add_separator:
            clean_layer_list += '|'
        should_add_separator = True
        clean_layer_list += 'tertiary'
    clean_layer_list += '"]'
    return clean_layer_list

def generate_map(city_name, radius, network_filter, river: bool, lake: bool):
    geolocator = Nominatim(user_agent="map_plotter")
    location = geolocator.geocode(city_name)
    place_metadata = geolocator.reverse(location.point)

    place_cleaned = city_name.replace(' ', '_').replace(',', '')

    EXPORT_DIR = Path("export") / place_cleaned
    TMP_DIR = Path("tmp") / place_cleaned
    EXPORT_DIR.mkdir(exist_ok=True, parents=True)

    # clean file tree

    for root, dirs, files in os.walk(TMP_DIR):
        for file in files:
            os.remove(os.path.join(root, file))

    map = Map((location.latitude, location.longitude), radius, network_filter, river, lake)

    generated_map = map.export_image(TMP_DIR / f"{place_cleaned}_map.svg")

    generate_canva((TMP_DIR / f"{place_cleaned}_map.svg").__str__(),
                   (EXPORT_DIR / f"{place_cleaned}_with_canva.svg"))

    return (EXPORT_DIR / f"{place_cleaned}_with_canva.svg").__str__()



