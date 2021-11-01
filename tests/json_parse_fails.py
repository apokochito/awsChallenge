import json
import pytest
import os
from unittest import mock
from lambda_function import lambda_handler

# Mocking ENV Variable
@pytest.fixture(autouse=True)
def mock_settings_env_vars():
    with mock.patch.dict(os.environ, {"LOGGER_LEVEL": "INFO"}):
        yield

def test_environment_variable():
    assert os.environ["LOGGER_LEVEL"] == "INFO"

@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return 1


def test_lambda_handler_json_parse_error(apigw_event, mocker):

    ret = lambda_handler(apigw_event, "")
    print(ret)

    assert ret["statusCode"] == 400