# register model

import json
import mlflow
from mlflow.tracking import MlflowClient
from src.logger import logging
import dagshub
import warnings
import os

warnings.simplefilter("ignore", UserWarning)
warnings.filterwarnings("ignore")


# Below code block is for production use
# -------------------------------------------------------------------------------------
# Set up DagsHub credentials for MLflow tracking
dagshub_token = os.getenv("CAPSTONE_TEST")
if not dagshub_token:
    raise EnvironmentError("CAPSTONE_TEST environment variable is not set")

os.environ["MLFLOW_TRACKING_USERNAME"] = dagshub_token
os.environ["MLFLOW_TRACKING_PASSWORD"] = dagshub_token

dagshub_url = "https://dagshub.com"
repo_owner = "shekhus"
repo_name = "capastan_sentiment_analysis"

# Set up MLflow tracking URI
mlflow.set_tracking_uri(f'{dagshub_url}/{repo_owner}/{repo_name}.mlflow')
# -------------------------------------------------------------------------------------
# ---------------------------------------------------------------------
# LOCAL USE
# ---------------------------------------------------------------------
# mlflow.set_tracking_uri(
#     "https://dagshub.com/shekhus/capastan_sentiment_analysis.mlflow"
# )
# dagshub.init(
#     repo_owner="shekhus",
#     repo_name="capastan_sentiment_analysis",
#     mlflow=True
# )
# ---------------------------------------------------------------------


def load_model_info(file_path: str) -> dict:
    """Load the model info from a JSON file."""
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except Exception as e:
        logging.error("Failed to load model info: %s", e)
        raise


def register_model(model_name: str, model_info: dict):
    """
    Register a new model version from an existing MLflow run.
    """
    try:
        run_id = model_info["run_id"]
        artifact_path = model_info["model_path"]

        model_uri = f"runs:/{run_id}/{artifact_path}"

        client = MlflowClient()

        model_version = client.create_model_version(
            name=model_name,
            source=model_uri,
            run_id=run_id
        )

        client.transition_model_version_stage(
            name=model_name,
            version=model_version.version,
            stage="Staging"
        )

        logging.info(
            "Model '%s' version %s registered and moved to Staging",
            model_name,
            model_version.version
        )

    except Exception as e:
        logging.error("Error during model registration: %s", e)
        raise


def main():
    try:
        model_info = load_model_info("reports/experiment_info.json")
        register_model("my_model", model_info)
    except Exception as e:
        logging.error("Model registration failed: %s", e)
        print(f"Error: {e}")


if __name__ == "__main__":
    main()





