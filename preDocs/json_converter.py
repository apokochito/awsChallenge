import json as js
import xml.etree.ElementTree as et
import logging
import boto3
import io
import os
from urllib.parse import urlparse

def loadJsonData(event):
    return js.loads(str(event.get('body')))
    
def buildXMLFile(a):
    return str(et.tostring(a.getroot(), encoding='utf8').decode('utf8'))

def putHeaders(et, header, event, data):
    et.SubElement(header, "echoToken").text = str(event.get('headers').get('correlationId'))
    et.SubElement(header, "timestamp").text = str(str(data["reservation"]["lastUpdateTimestamp"]))
    
def putBody(et, body, data, r):
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
    return a

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    try:
        logger = logging.getLogger()
        logger.setLevel(os.environ['LOG_LEVEL'])
        
        logger.info('## CORRELATION ID ##')
        logger.info(event.get('headers').get('correlationId'))
        logger.info('## USER ##')
        logger.info(event.get('headers').get('user'))
        
        # Load JSON data
        data = loadJsonData(event)
        logger.info('## JSON RECEIVED ##')
        logger.info(data)
        
        # Put main tags
        r = et.Element("Reservation")
        header = et.SubElement(r, "header")
        body = et.SubElement(r, "body")
        
        # Put headers
        putHeaders(et, header, event, data)
        
        # Put body
        a = putBody(et, body, data, r)
    
        # Build string XML
        stringXML = buildXMLFile(a)
        logger.info('## XML TRANSFORMED ##')
        logger.info(stringXML)
        
        # Upload object to S3
        bucketName='sam-demo-cloudformation-1'
        bucketKey='new_file.xml'
        boto3.client('s3').put_object(Bucket='sam-demo-cloudformation-1', Body=stringXML, Key='new_file.xml')
        logger.info('## S3 URL ##')
        logger.info('https://sam-demo-cloudformation-1.s3.amazonaws.com/new_file.xml')
    except Exception as inst:
        # Error message
        logger.error('## FAILURE ##')
        logger.error(str(inst))
        # HTTP error response
        return { 'statusCode': 400, 'body': 'There\'s an error processing your JSON body.' }
    return {
    'statusCode': 200,
    'body': 'https://sam-demo-cloudformation-1.s3.amazonaws.com/new_file.xml'
    }
