#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import requests
from flask import Flask

river_level = Flask(__name__)
graph_link = "http://water.weather.gov/resources/hydrographs/rmdv2_hg.png"


@river_level.route('/level')
def level_val():
    return main()


@river_level.route('/link')
def level_link():
    return graph_link


def main():
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


if __name__ == "__main__":
    """ This is executed when run from the command line """
    river_level.run(debug=True, host='0.0.0.0')
