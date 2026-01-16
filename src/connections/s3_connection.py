import logging
import boto3
import pandas as pd
from io import StringIO
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)


class s3_operations:
    """
    S3 operations using AWS Credential Provider Chain.
    No credentials are hardcoded or passed explicitly.
    """

    def __init__(self, bucket_name: str, region: str = "ap-south-1"):
        self.bucket_name = bucket_name

        try:
            self.s3_client = boto3.client(
                "s3",
                region_name=region
            )
            logger.info(
                "S3 client initialized using AWS credential provider chain"
            )

        except Exception as e:
            logger.error("Failed to initialize S3 client: %s", e)
            raise

    def fetch_file_from_s3(self, file_key: str) -> pd.DataFrame:
        """
        Fetch CSV file from S3 and return as Pandas DataFrame
        """
        try:
            logger.info(
                "Fetching file '%s' from S3 bucket '%s'...",
                file_key,
                self.bucket_name
            )

            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_key
            )

            csv_data = response["Body"].read().decode("utf-8")
            df = pd.read_csv(StringIO(csv_data))

            # ✅ YOUR REQUIRED LOG MESSAGE (ADDED)
            logger.info(
                "Successfully fetched and loaded '%s' from S3 that has %d records.",
                file_key,
                len(df)
            )

            return df

        except ClientError as e:
            logger.error("AWS Client error while fetching '%s': %s", file_key, e)
            raise

        except Exception as e:
            logger.error(
                "Unexpected error while fetching '%s' from S3: %s",
                file_key,
                e
            )
            raise
