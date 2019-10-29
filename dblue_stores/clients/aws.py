import boto3
from decouple import config

from .base import BaseClient


class AwsClient(BaseClient):
    @classmethod
    def get_client(cls, *args, **kwargs):
        return cls._get_client(*args, **kwargs)

    @staticmethod
    def get_legacy_api(legacy_api=False):
        legacy_api = legacy_api or config("AWS_LEGACY_API", default=False, cast=bool)
        return legacy_api

    @staticmethod
    def get_session(aws_access_key_id=None,
                    aws_secret_access_key=None,
                    aws_session_token=None,
                    region_name=None):

        aws_access_key_id = aws_access_key_id or config("AWS_ACCESS_KEY_ID", default=None)
        aws_secret_access_key = aws_secret_access_key or config("AWS_SECRET_ACCESS_KEY", default=None)
        aws_session_token = aws_session_token or config("AWS_SECURITY_TOKEN", default=None)
        region_name = region_name or config("AWS_REGION", default=None)

        return boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name
        )

    @classmethod
    def _get_client(cls,
                    client_type,
                    endpoint_url=None,
                    aws_access_key_id=None,
                    aws_secret_access_key=None,
                    aws_session_token=None,
                    region_name=None,
                    aws_use_ssl=True,
                    aws_verify_ssl=None):

        session = cls.get_session(aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  aws_session_token=aws_session_token,
                                  region_name=region_name)

        endpoint_url = endpoint_url or config("AWS_ENDPOINT_URL", default=None)
        aws_use_ssl = aws_use_ssl or config("AWS_USE_SSL", default=True, cast=bool)

        if aws_verify_ssl is None:
            aws_verify_ssl = config("AWS_VERIFY_SSL", default=True, cast=bool)
        else:
            aws_verify_ssl = aws_verify_ssl

        return session.client(
            client_type,
            endpoint_url=endpoint_url,
            use_ssl=aws_use_ssl,
            verify=aws_verify_ssl)

    @classmethod
    def get_resource(cls,
                     resource_type,
                     endpoint_url=None,
                     aws_access_key_id=None,
                     aws_secret_access_key=None,
                     aws_session_token=None,
                     region_name=None,
                     aws_use_ssl=True,
                     aws_verify_ssl=None):
        session = cls.get_session(aws_access_key_id=aws_access_key_id,
                                  aws_secret_access_key=aws_secret_access_key,
                                  aws_session_token=aws_session_token,
                                  region_name=region_name)

        endpoint_url = endpoint_url or config("AWS_ENDPOINT_URL", default=None)
        aws_use_ssl = aws_use_ssl or config("AWS_USE_SSL", default=True, cast=bool)

        if aws_verify_ssl is None:
            aws_verify_ssl = config("AWS_VERIFY_SSL", default=True, cast=bool)
        else:
            aws_verify_ssl = aws_verify_ssl

        return session.resource(
            resource_type,
            endpoint_url=endpoint_url,
            use_ssl=aws_use_ssl,
            verify=aws_verify_ssl)