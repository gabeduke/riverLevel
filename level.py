#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import requests
import re

from bs4 import BeautifulSoup
from flask import Flask

river_level = Flask(__name__)
level_graph_link = "http://water.weather.gov/resources/hydrographs/rmdv2_hg.png"


@river_level.route('/level')
def level_val():
    return level()


@river_level.route('/level/link')
def level_link():
    return level_graph_link


@river_level.route('/temp')
def level_temp():
    return temp()


@river_level.route('/temp/link')
def temp_link():
    return temp_graph_link


def temp():
    return trueOO


def level():
    # Gather XML Data
    link = "http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2&output=xml"
    xmlString = requests.get(link).text

    # Parse XML Data
    root = ET.fromstring(xmlString)

    # Parse Latest Reading
    latest = root.find("./observed/datum")
    reading = latest.find("primary").text

    # Print latest reading
    reading_str = "River Level is: {}".format(reading)

    return "{}".format(reading_str)


@river_level.route('/links')
def get_image_links():

    link = "https://waterdata.usgs.gov/nwis/uv?cb_00010=on&cb_00060=on&format=gif_stats&site_no=02035000&period=7"

    page = requests.get(link)
    soup = BeautifulSoup(page.text, 'html.parser')
    imgs = soup.findAll('img')
    links = []

    for img in imgs:
        if (re.search('02035000', str(img))):
            links.append(img['src'])

    pprint = (', '.join(links))
    return pprint


if __name__ == "__main__":
    """ This is executed when run from the command line """
    river_level.run(debug=True, host='0.0.0.0')
