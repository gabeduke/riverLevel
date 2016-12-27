import xml.etree.ElementTree as ET
import requests

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
