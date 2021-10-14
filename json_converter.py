#!/usr/bin/env python3

import json as js
import xml.etree.ElementTree as et
import logging as logger

def processXml():
    logger.debug('Transforming JSON file...')
    r = et.Element("Reservation")
        
    header = et.SubElement(r, "header")
    body = et.SubElement(r, "body")

    et.SubElement(header, "echoToken").text = data["header"]["echoToken"]
    et.SubElement(header, "timestamp").text = data["header"]["timestamp"]

    hotel = et.SubElement(body, "hotel")
    et.SubElement(hotel, "uuid").text = data["reservation"]["hotel"]["uuid"]
    et.SubElement(hotel, "code").text = data["reservation"]["hotel"]["code"]
    et.SubElement(hotel, "offset").text = data["reservation"]["hotel"]["offset"]

    et.SubElement(body, "reservationId").text = str(data["reservation"]["reservationId"])

    reservations = et.SubElement(body, "reservations")

    for z in data["reservation"]["confirmationNumbers"]:
        reservation = et.SubElement(reservations, "reservation")
        reservation.set("source", z["source"])
        info = et.SubElement(reservation, "info")
        info.set("confirmationNumber", z["confirmationNumber"])
        fullName = z["guest"]
        et.SubElement(info, "firstName").text = fullName.split(' ')[0]
        et.SubElement(info, "lastName").text = fullName.split(' ')[1]

    et.SubElement(body, "lastUpdateTimestamp").text = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(body, "lastUpdateOperatorId").text = str(data["reservation"]["lastUpdateOperatorId"])

    a = et.ElementTree(r)
    logger.info('JSON file transformed.')

    try:
        logger.debug('Creating XML file...')
        a.write("new_file.xml", encoding="utf-8")
        logger.info('XML file created.')
    except:
        logger.error('There\'s an error in writing your XML file.')

try:
    with open("input.json", encoding="utf-8") as json_file:
        logger.debug('Loading JSON file...')
        data = js.load(json_file)
        logger.debug('Closing JSON file...')
        json_file.close()
        logger.info('Valid input JSON file.')
        processXml()
except:
    logger.error('There\'s an error with you JSON file, it cannot be read.')
