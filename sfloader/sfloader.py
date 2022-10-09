from sfloader.credentials import Credentials
from sfloader.job import Job

class SForce:
    def __init__(self, grant_type, client_id, client_secret,
                 username, password, api_version, host,
    ):
        self.credentials = Credentials(grant_type=grant_type, client_id=client_id,
                             client_secret=client_secret, username=username,
                             password=password, api_version=api_version,
                             host=host)

        self.credentials.retrieve()

    def upload(self, file, object_type, report_builder, external_key, operation, line_ending):
        job = Job(credentials=self.credentials, report_builder=report_builder)
        job.create(object_type=object_type, operation=operation,
                        line_ending=line_ending, external_key=external_key)
        job.upload_file(file)
        job.finalize()
        job.check_status()
