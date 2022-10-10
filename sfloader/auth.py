import requests
from sfloader.exceptions import AuthError


class SFAuthPassword:
    access_token = None
    instance_url = None

    def __init__(
        self,
        grant_type,
        client_id,
        client_secret,
        username,
        password,
        api_version,
        host,
    ):
        self.api_version = api_version
        self.grant_type = grant_type
        self.client_id = client_id
        self.client_secret = client_secret
        self.username = username
        self.password = password
        self.host = host

    def connect(self):
        response = requests.post(
            url=self.oauth_url,
            data={
                "grant_type": self.grant_type,
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "username": self.username,
                "password": self.password,
            },
        )

        if response.status_code != 200:
            raise AuthError("Error retrieve access token")

        data = response.json()

        self.access_token = data["access_token"]
        self.instance_url = data["instance_url"]
        return self

    @property
    def oauth_url(self):
        return f"https://{self.host}/services/oauth2/token"

    @property
    def auth_header(self):
        return {"Authorization": f"Bearer {self.access_token}"}
