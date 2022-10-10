from sfloader.io_report import IOReport
from sfloader.job import Job
from sfloader.logger import Logger


class SFLoader:
    def __init__(self, auth_client):
        self.auth_client = auth_client.connect()

    def upload(
        self,
        file,
        object_type,
        operation,
        line_ending="LF",
        report_builder=IOReport(),
        external_key=None,
        silent=False,
    ):
        logger = Logger(silent=silent)
        job = Job(
            auth_client=self.auth_client, report_builder=report_builder, logger=logger
        )
        job.create(
            object_type=object_type,
            operation=operation,
            line_ending=line_ending,
            external_key=external_key,
        )
        job.upload_file(file)
        job.finalize()
        job.check_status()
