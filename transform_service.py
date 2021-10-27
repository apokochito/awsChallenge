import json as js
import xml.etree.ElementTree as et
import logging

def load_json_data(event):
    body = str(event.get('body'))
    logging.debug('Receiving JSON body: ', body)
    data = js.loads(body)
    return data

def get_echo_token(event):
    echo_token = event.get('headers').get('correlationId')
    return echo_token

def put_headers(event, header, data):
    echoToken = event.get('headers').get('correlationId')
    timestamp = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(header, "echoToken").text = str(echoToken)
    et.SubElement(header, "timestamp").text = str(timestamp)

def put_body(data, body, r):
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
    