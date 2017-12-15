#!/usr/bin/env python3
import xml.etree.ElementTree as ET
import requests


def main():
  # Gather XML Data
  link = "http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2&output=xml"
  xmlString = requests.get(link).text

  # Parse XML Data
  root = ET.fromstring(xmlString)

  # Parse Latest Reading
  latest = root.find("./observed/datum")


  # Print latest reading
  print("River Level is: " + latest.find("primary").text)
  print("http://water.weather.gov/resources/hydrographs/rmdv2_hg.png")


if __name__ == "__main__":
    """ This is executed when run from the command line """
    main()
    
