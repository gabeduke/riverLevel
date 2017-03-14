#!/usr/bin/env python
import io
import logging
import os
import xml.etree.ElementTree as ET
import aiohttp
import requests
import plugins

logger = logging.getLogger(__name__)


def _initialise(bot):
    plugins.register_user_command(['level', 'riverLevel'])


def level(bot, event):
    # Gather XML Data
    link = "http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2&output=xml"
    link_image = "http://water.weather.gov/resources/hydrographs/rmdv2_hg.png"
    xmlString = requests.get(link).text

    # Parse XML Data
    root = ET.fromstring(xmlString)

    # Parse Latest Reading
    latest = root.find("./observed/datum")

    logger.info("getting {}".format(link_image))

    filename = os.path.basename(link_image)
    r = yield from aiohttp.request('get', link_image)
    raw = yield from r.read()
    image_data = io.BytesIO(raw)

    image_id = yield from bot._client.upload_image(image_data, filename=filename)

    yield from bot.coro_send_message(event.conv.id_, "River Level is: " + latest.find("primary").text, None, None)
    yield from bot.coro_send_message(event.conv.id_, None, image_id=image_id)

    # Print latest reading
    print("River Level is: " + latest.find("primary").text)
    # print("http://water.weather.gov/resources/hydrographs/rmdv2_hg.png")
