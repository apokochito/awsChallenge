import xml.etree.ElementTree as et
import logging
import io
import transform_service
import os
import s3_client

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    # Load JSON data
    try:
        logging.setLevel(os.environ['LOG_LEVEL'])
        data = transform_service.load_json_data(event)
    except Exception as inst:
        logging.error(str(inst))
        logging.error('There\'s an error loading your JSON body.')
        return { 'statusCode': 400, 'body': 'Error while loading JSON object.' }
        
    # Transform JSON to XML Tree
    try:
        logging.debug('Transforming JSON body...')
        r = et.Element("Reservation")
        header = et.SubElement(r, "header")
        body = et.SubElement(r, "body")
        
        transform_service.put_headers(event, data)

        tree = transform_service.put_body(data)
        
        result = transform_service.build_xml_file(tree)
    except Exception as inst:
        logging.error(str(inst))
        logging.error('There\'s an error transforming your JSON body.')
        return { 'statusCode': 500, 'body': 'Error while transforming JSON object.' }

    # Update file
    try:
        s3_client.update_file(result)
    except Exception as inst:
        logging.error(str(inst))
        logging.error('There\'s an error updating your JSON body.')
        return { 'statusCode': 500, 'body': 'Error while updating JSON object.' }
    
    return { 'statusCode': 200, 'body': 'https://sam-demo-cloudformation-1.s3.amazonaws.com/new_file.xml' }
