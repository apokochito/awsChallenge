import json as js
import xml.etree.ElementTree as et
import logging as logger
import boto3
import io
from urllib.parse import urlparse

s3 = boto3.resource('s3')

def loadJsonData(event):
    logger.debug('Receiving JSON body...')
    other = str(event.get('body'))
    data = js.loads(other)
    logger.info('Valid input JSON body.')
    return data

def putHeaders(event, data):
    echoToken = event.get('headers').get('correlationId')
    timestamp = str(data["reservation"]["lastUpdateTimestamp"])
    et.SubElement(header, "echoToken").text = str(echoToken)
    et.SubElement(header, "timestamp").text = str(timestamp)

def putBody(data):
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
    logger.info('JSON body transformed.')
    return a

def buildXMLFile(a):
    logger.debug('Creating XML file...')
    root = a.getroot()
    hi = et.tostring(root, encoding='utf8').decode('utf8')
    resul = str(hi)
    logger.info('XML file created.')
    return resul

def lambda_handler(event, context):
    try:
        # Load JSON data
        data = loadJsonData(event)
        
        # Transform JSON to XML Tree
        logger.debug('Transforming JSON body...')
        r = et.Element("Reservation")
        header = et.SubElement(r, "header")
        body = et.SubElement(r, "body")
        
        # Put Headers in XMl Tree
        putHeaders(event, data)
        
        # Put Body in XMl Tree
        a = putBody(data)
        
        # Build XML file
        resul = buildXMLFile(a)
        
        # Upload XML file to S3
        boto3.client('s3').put_object(Bucket='sam-demo-cloudformation-1', Body=resul, Key='new_file.xml')
        
    except Exception as inst:
        logger.error(str(inst))
        logger.error('There\'s an error processing your JSON body.')    
    
    return { 'statusCode': 200, 'body': 'https://sam-demo-cloudformation-1.s3.amazonaws.com/new_file.xml' }