import xml.etree.ElementTree as et
import logging
import io
import transform_service
import os
import s3_client

def lambda_handler(event, context):
    # Load JSON data
    try:
        logger = logging.getLogger()
        logger.setLevel(os.environ['LOGGER_LEVEL'])
        data = transform_service.load_json_data(event)
    except Exception as inst:
        logger.error(str(inst))
        logger.error('There\'s an error loading your JSON body.')
        return { 'statusCode': 400, 'body': 'Error while loading JSON object.' }
        
    # Transform JSON to XML Tree
    try:
        logger.debug('Transforming JSON body...')
        r = et.Element("Reservation")
        header = et.SubElement(r, "header")
        body = et.SubElement(r, "body")
        
        transform_service.put_headers(event, header, data)

        tree = transform_service.put_body(data, body, r)
        
        result = transform_service.build_xml_file(tree)
    except Exception as inst:
        logger.error(str(inst))
        logger.error('There\'s an error transforming your JSON body.')
        return { 'statusCode': 500, 'body': 'Error while transforming JSON object.' }

    # Update file
    try:
        file_name = transform_service.get_echo_token(event)
        s3_client.update_file(result, file_name)
    except Exception as inst:
        logger.error(str(inst))
        logger.error('There\'s an error updating your JSON body.')
        return { 'statusCode': 500, 'body': 'Error while updating JSON object.' }
    
    return { 'statusCode': 200, 'body': 'https://sam-demo-cloudformation-1.s3.amazonaws.com/new_file.xml' }
