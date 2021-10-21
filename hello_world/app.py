import json as js
import xml.etree.ElementTree as et
import logging as logger
import boto3
import io

s3 = boto3.client("s3")

def lambda_handler(event, context):
    try:
        logger.debug('Receiving JSON body...')
        data = js.loads(event['body'])
        logger.info('Valid input JSON body.')
        logger.debug('Transforming JSON body...')
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
            et.SubElement(info, "firstName").text = fullName
            et.SubElement(info, "lastName").text = fullName

        et.SubElement(body, "lastUpdateTimestamp").text = str(data["reservation"]["lastUpdateTimestamp"])
        et.SubElement(body, "lastUpdateOperatorId").text = str(data["reservation"]["lastUpdateOperatorId"])
        a = et.ElementTree(r)
        logger.info('JSON body transformed.')
    
        try:
            logger.debug('Creating XML file...')
            root = a.getroot()
            hi = et.tostring(root, encoding='utf8').decode('utf8')
            resul = str(hi)
            s3.put_object(Bucket='sam-demo-cloudformation-1', Body=resul, Key='new_file.xml')
            logger.info('XML file created.')
        except Exception as inst:
            logger.error(str(inst))
            logger.error('There\'s an error in writing your XML file.')
            
    except:
        logger.error('There\'s an error with you JSON body, it cannot be read.')
    return {
    'statusCode': 200,
    'body': 'https://sam-demo-cloudformation-1.s3.us-east-1.amazonaws.com/new_file.xml'
    }
