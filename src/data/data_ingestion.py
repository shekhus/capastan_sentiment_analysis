# data ingestion

import os
import numpy as np
import pandas as pd
pd.set_option('future.no_silent_downcasting', True)

from sklearn.model_selection import train_test_split
import yaml
from dotenv import load_dotenv

from src.logger import logging
from src.connections import s3_connection

# --------------------------------------------------------------------
# ENV SETUP
# --------------------------------------------------------------------

load_dotenv()

# --------------------------------------------------------------------
# CONFIG LOADERS
# --------------------------------------------------------------------

def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file."""
    try:
        with open(params_path, "r") as file:
            params = yaml.safe_load(file)
        logging.debug("Parameters retrieved from %s", params_path)
        return params
    except Exception as e:
        logging.error("Failed to load params.yaml: %s", e)
        raise


def load_data_from_url(data_url: str) -> pd.DataFrame:
    """Load data from public URL (development mode)."""
    try:
        logging.info("Loading data from URL: %s", data_url)
        df = pd.read_csv(data_url)
        logging.info("Successfully loaded data from URL with %d records", len(df))
        return df
    except Exception as e:
        logging.error("Failed to load data from URL: %s", e)
        raise


def load_data_from_s3(file_key: str) -> pd.DataFrame:
    """Load data from AWS S3 (production mode)."""
    bucket_name = os.getenv("AWS_BUCKET_NAME")
    region = os.getenv("AWS_REGION", "ap-south-1")

    if not bucket_name:
        raise EnvironmentError("AWS_BUCKET_NAME is not set")

    s3 = s3_connection.s3_operations(
        bucket_name=bucket_name,
        region=region
    )

    return s3.fetch_file_from_s3(file_key)


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """Preprocess the data."""
    try:
        logging.info("Pre-processing started")

        final_df = df.loc[df["sentiment"].isin(["positive", "negative"])].copy()
        final_df["sentiment"] = final_df["sentiment"].map(
            {"positive": 1, "negative": 0}
        )

        logging.info("Pre-processing completed")
        return final_df

    except Exception as e:
        logging.error("Preprocessing failed: %s", e)
        raise


def save_data(
    train_data: pd.DataFrame,
    test_data: pd.DataFrame,
    data_path: str
) -> None:
    """Save train and test datasets."""
    try:
        raw_data_path = os.path.join(data_path, "raw")
        os.makedirs(raw_data_path, exist_ok=True)

        train_data.to_csv(os.path.join(raw_data_path, "train.csv"), index=False)
        test_data.to_csv(os.path.join(raw_data_path, "test.csv"), index=False)

        logging.info("Train and test data saved at %s", raw_data_path)

    except Exception as e:
        logging.error("Failed to save data: %s", e)
        raise


# --------------------------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------------------------

def main():
    try:
        params = load_params("params.yaml")
        test_size = params["data_ingestion"]["test_size"]

        # ------------------------------------------------------------
        # DATA SOURCE SWITCH (URL | S3)
        # ------------------------------------------------------------

        data_source = os.getenv("DATA_SOURCE", "URL").upper()

        if data_source == "S3":
            logging.info("Data source set to S3")
            df = load_data_from_s3("data.csv")

        else:
            logging.info("Data source set to URL (development mode)")
            df = load_data_from_url(
                "https://raw.githubusercontent.com/vikashishere/Datasets/refs/heads/main/data.csv"
            )

        # ------------------------------------------------------------
        # PROCESSING
        # ------------------------------------------------------------

        final_df = preprocess_data(df)

        train_data, test_data = train_test_split(
            final_df,
            test_size=test_size,
            random_state=42,
            stratify=final_df["sentiment"]
        )

        save_data(train_data, test_data, data_path="./data")

        logging.info("Data ingestion pipeline completed successfully")

    except Exception as e:
        logging.error("Data ingestion failed: %s", e)
        raise


if __name__ == "__main__":
    main()
