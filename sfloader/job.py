import csv
import time
import requests
from sfloader.exceptions import SalesforceError


class Job:
    job_id = None
    content_url = None
    object_type = None
    external_key = None

    def __init__(self, auth_client, report_builder, logger):
        self.logger = logger
        self.report_builder = report_builder
        self.auth_client = auth_client
        self.jobs_url = f"{self.auth_client.instance_url}/services/data/v{self.auth_client.api_version}/jobs/ingest"

    def create(self, object_type, operation, external_key=None, line_ending="LF"):
        response = requests.post(
            url=self.jobs_url,
            headers={
                **self.auth_client.auth_header,
                "Content-Type": "application/json",
                "X-PrettyPrint": "1",
            },
            json={
                "contentType": "CSV",
                "object": object_type,
                "operation": operation,
                "lineEnding": line_ending,
                "externalIdFieldName": external_key,
            },
        )

        if response.status_code > 201:
            raise SalesforceError(f"Error retrieve access token: {response.content}")

        result = response.json()

        self.job_id = result["id"]
        self.content_url = result["contentUrl"]
        self.logger.log(f"Job ID {self.job_id} created")

    def upload_file(self, file):
        try:
            name = file.name
        except AttributeError:
            name = "..."

        self.logger.log(f"Uploading file {name}")

        response = requests.put(
            url=f"{self.auth_client.instance_url}/{self.content_url}",
            data=file.read().encode("utf-8"),
            headers={
                **self.auth_client.auth_header,
                "Content-Type": "text/csv",
            },
        )

        if response.status_code > 201:
            raise SalesforceError(f"Error file upload: {response.content}")

    def finalize(self):
        response = requests.patch(
            url=f"{self.jobs_url}/{self.job_id}",
            headers={
                **self.auth_client.auth_header,
                "Content-Type": "application/json",
                "X-PrettyPrint": "1",
            },
            json={"state": "UploadComplete"},
        )

        if response.status_code > 201:
            raise SalesforceError(f"Error finalize job: {response.content}")

    def check_status(self):
        self.logger.log("Check job status")

        response = requests.get(
            url=f"{self.jobs_url}/{self.job_id}",
            headers={
                **self.auth_client.auth_header,
                "Content-Type": "application/json",
                "X-PrettyPrint": "1",
            },
        )

        if response.status_code != 200:
            raise SalesforceError(f"Error job monitoring: {response.content}")

        result = response.json()

        if result["state"] == "Failed":
            raise SalesforceError(f"Job processing failed: {result}")

        if result["state"] == "JobComplete":
            self.logger.log(
                "\nJop complete! Report in progress.",
            )
            self.handle_report("success")
            self.handle_report("failure")
            return None

        time.sleep(3)
        self.check_status()

    def handle_report(self, status):
        key = "successfulResults" if status == "success" else "failedResults"
        response = requests.get(
            url=f"{self.jobs_url}/{self.job_id}/{key}",
            headers={
                **self.auth_client.auth_header,
                "Accept": "text/csv",
            },
        )

        if response.status_code > 299:
            raise SalesforceError(f"Download report error: {response.content}")

        csv_rows = csv.reader(
            response.content.decode("utf-8").splitlines(), delimiter=","
        )
        self.report_builder.call(status, list(csv_rows))
