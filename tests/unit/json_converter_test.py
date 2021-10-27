import json
import boto3
import pytest
from moto import mock_s3
import unittest
from hello_world import app

@mock_s3
def test_my_model_save():
    pass