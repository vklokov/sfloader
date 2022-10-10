import csv
import time
import requests
from sfloader.exceptions import SalesforceError


class Job:
    job_id = None
    content_url = None
    object_type = None
    external_key = None

    def __init__(self, credentials, report_builder):
        self.report_builder = report_builder
        self.credentials = credentials
        self.jobs_url = f"{self.credentials.instance_url}/services/data/v{self.credentials.api_version}/jobs/ingest"

    def create(self, object_type, operation, external_key=None, line_ending="LF"):
        response = requests.post(
            url=self.jobs_url,
            headers={
                **self.credentials.auth_header,
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

    def upload_file(self, file):
        response = requests.put(
            url=f"{self.jobs_url}/#{self.job_id}/batches",
            data=file.read().encode("utf-8"),
            headers={
                **self.credentials.auth_header,
                "Content-Type": "text/csv",
            },
        )

        if response.status_code > 201:
            raise SalesforceError(f"Error file upload: {response.content}")

    def finalize(self):
        response = requests.post(
            url=f"{self.jobs_url}/#{self.job_id}",
            headers={
                **self.credentials.auth_header,
                "Content-Type": "application/json",
                "X-PrettyPrint": "1",
            },
            json={"state": "UploadComplete"},
        )

        if response.status_code > 201:
            raise SalesforceError(f"Error retrieve access token: {response.content}")

    def check_status(self):
        response = requests.get(
            url=f"{self.jobs_url}/{self.job_id}",
            headers={
                **self.credentials.auth_header,
                "Content-Type": "application/json",
                "X-PrettyPrint": "1",
            },
        )

        if response.status_code != 200:
            raise SalesforceError(f"Error job monitoring: {response.content}")

        result = response.json()

        if result["state"] == "Failed":
            raise SalesforceError("Job processing failed")

        if result["state"] == "JobComplete":
            self.handle_report("success")
            self.handle_report("failure")

        time.sleep(3)
        self.check_status()

    def handle_report(self, status):
        key = "successfulResults" if status == "success" else "failedResults"
        response = requests.get(
            url=f"{self.jobs_url}/{self.job_id}/{key}",
            headers={
                **self.credentials.auth_header,
                "Accept": "text/csv",
            },
        )

        if response.status_code > 299:
            raise SalesforceError(f"Download report error: {response.content}")

        csv_rows = csv.reader(
            response.content.decode("utf-8").splitlines(), delimiter=","
        )
        self.report_builder.call(status, list(csv_rows))
