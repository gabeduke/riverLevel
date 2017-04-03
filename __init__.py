#!/usr/bin/env python
import io
import logging
import os
import xml.etree.ElementTree as ET
import aiohttp
import requests
import plugins
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def _initialise(bot):
    plugins.register_user_command(['level'])


def level(bot, event, *args):
    # Gather XML Data
    level_http_link = "http://water.weather.gov/ahps2/hydrograph_to_xml.php?gage=rmdv2&output=xml"
    level_image_link = "http://water.weather.gov/resources/hydrographs/rmdv2_hg.png"
    temp_image_link = "https://waterdata.usgs.gov/nwisweb/graph?agency_cd=USGS&site_no=02035000&parm_cd=00010&period=7"
    level_xml_string = requests.get(level_http_link).text

    level_file = os.path.basename(level_image_link)
    level_image_data = image_downloader(level_image_link)

    temp_file = os.path.basename(temp_image_link)
    temp_image_data = image_downloader(temp_image_link)

    # Parse XML Data
    root = ET.fromstring(level_xml_string)

    # Parse Latest Reading
    latest = root.find("./observed/datum")

    logger.info("getting {}".format(level_image_link))

    level_image_id = yield from bot._client.upload_image(level_image_data, filename=level_file)
    temp_image_id = yield from bot._client.upload_image(temp_image_data, filename=temp_file)

    yield from bot.coro_send_message(event.conv.id_, "River Level is: " + latest.find("primary").text, None, None)
    yield from bot.coro_send_message(event.conv.id_, None, image_id=level_image_id)
    yield from bot.coro_send_message(event.conv.id_, None, image_id=temp_image_id)


def image_downloader(link):
    level_file = os.path.basename(link)
    r = yield from aiohttp.request('get', link)
    raw = yield from r.read()
    return io.BytesIO(raw)
