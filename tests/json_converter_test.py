import json
import boto3
import pytest
from moto import mock_s3
import unittest
from s3_client import boto3

@mock_s3
def test_my_model_save():
    pass