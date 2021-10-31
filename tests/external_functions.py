import json
import pytest
import os
from unittest import mock
from lambda_function import lambda_handler
import transform_service
import xml.etree.ElementTree as et
from xml.etree import ElementTree, ElementInclude

# Mocking ENV Variable
@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"LOGGER_LEVEL": "INFO"}):
        yield

def test_environment_variable():
    assert os.environ["LOGGER_LEVEL"] == "INFO"

data = {"reservation":{"hotel":{"uuid":"3_c5f3c903-c43d-4967-88d1-79ae81d00fcb","code":"TASK1","offset":"+06:00"},"reservationId":12345,"confirmationNumbers":[{"confirmationNumber":"12345","source":"ENCORA","guest":"Arturo Vargas"},{"confirmationNumber":"67890","source":"NEARSOFT","guest":"Carlos Hernández"}],"lastUpdateTimestamp":"2018-03-0720:59:541Z","lastUpdateOperatorId":"task.user"}}

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {
        "body": data,
        "requestContext": {
            "resourceId": "123456",
            "apiId": "1234567890",
            "resourcePath": "/{proxy+}",
            "httpMethod": "POST",
            "requestId": "c6af9ac6-7b61-11e6-9a41-93e8deadbeef",
            "accountId": "123456789012"},
        "headers": {
            "user": "diana",
            "echoToken": "907f44fc-6b51-4237-8018-8a840fd87f04",
            "Via": "1.1 08f323deadbeefa7af34d5feb414ce27.cloudfront.net (CloudFront)",
            "Accept-Language": "en-US,en;q=0.8",
            "CloudFront-Is-Desktop-Viewer": "true",
            "CloudFront-Is-SmartTV-Viewer": "false",
            "CloudFront-Is-Mobile-Viewer": "false",
            "X-Forwarded-For": "127.0.0.1, 127.0.0.2",
            "CloudFront-Viewer-Country": "US",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Upgrade-Insecure-Requests": "1",
            "X-Forwarded-Port": "443",
            "Host": "1234567890.execute-api.us-east-1.amazonaws.com",
            "X-Forwarded-Proto": "https",
            "X-Amz-Cf-Id": "aaaaaaaaaae3VYQb9jd-nvCd-de396Uhbp027Y2JvkCPNLmGJHqlaA==",
            "CloudFront-Is-Tablet-Viewer": "false",
            "Cache-Control": "max-age=0",
            "User-Agent": "Custom User Agent String",
            "CloudFront-Forwarded-Proto": "https",
            "Accept-Encoding": "gzip, deflate, sdch"
        },
        "pathParameters": {"proxy": "/v1/reservations"},
        "httpMethod": "POST",
        "path": "/v1/reservations"
    }


def test_lambda_handler_external_function(apigw_event, mocker):

    ret = lambda_handler(apigw_event, "")
    print(ret)

    assert transform_service.get_echo_token(apigw_event) == "907f44fc-6b51-4237-8018-8a840fd87f04"

    r = et.Element("Reservation")
    header = et.SubElement(r, "header")
    body = et.SubElement(r, "body")
    tree = transform_service.put_body(data, body, r)
    result = transform_service.build_xml_file(tree)

    expect = et.tostring(result)

    assert expect == ""
    assert ret["statusCode"] == 200





