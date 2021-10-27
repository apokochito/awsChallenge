import json as js
import xml.etree.ElementTree as et
import logging

def load_json_data(event):
    body = str(event.get('body'))
    logging.debug('Receiving JSON body: ', body)
    data = js.loads(body)
    return data

def put_headers(event, data):
    echo_token = event.get('headers').get('correlationId')
    timestamp = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(header, "echo_token").text = str(echo_token)
    et.SubElement(header, "timestamp").text = str(timestamp)

def put_body(data):
    hotel = et.SubElement(body, "hotel")
    reservation_hotel = data["reservation"]["hotel"]
    et.SubElement(hotel, "uuid").text = reservation_hotel["uuid"]
    et.SubElement(hotel, "code").text = reservation_hotel["code"]
    et.SubElement(hotel, "offset").text = reservation_hotel["offset"]
    et.SubElement(body, "reservationId").text = str(data["reservation"]["reservationId"])
    reservations = et.SubElement(body, "reservations")
    for z in data["reservation"]["confirmationNumbers"]:
        reservation = et.SubElement(reservations, "reservation")
        reservation.set("source", z["source"])
        info = et.SubElement(reservation, "info")
        info.set("confirmationNumber", z["confirmationNumber"])
        full_name = z["guest"]
        et.SubElement(info, "firstName").text = full_name.split(' ')[0]
        et.SubElement(info, "lastName").text = full_name.split(' ')[1]

    et.SubElement(body, "lastUpdateTimestamp").text = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(body, "lastUpdateOperatorId").text = str(data["reservation"]["lastUpdateOperatorId"])
    tree = et.ElementTree(r)
    logging.debug('JSON body transformed.', tree)
    return tree

def build_xml_file(tree):
    logging.debug('Creating XML file...')
    root = tree.getroot()
    xml_encoded_file = et.tostring(root, encoding='utf8').decode('utf8')
    result = str(xml_encoded_file)
    logging.info('XML file created.')
    return result
    