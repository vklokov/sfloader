# Salesforce bulk uploader

## Installition

```bash
pip install git+https://github.com/vklokov/sfloader@master
```

## Usage

Initialize loader. Currently implemented only password auth method.

```python
from sfloader import SFLoader

loader = SFLoader(
    grant_type="password",
    client_id="CLIENT ID",
    client_secret="CLIENT SECRET",
    username="username",
    password="password",
    api_version="55.0",
    host="your-company-name.my.salesforce.com",
)
```

Provider report CSV & desired report builder (io report by default selected)

```python
...
from sfloader import FileReport

loader=SFLoader(...)

# Also StringIO (in memory) files are supported
with open("path/to/csv-file.csv", "r") as csvfile:
  loader.upload(
      file=csvfile,
      object_type="Account", # Salesforce entity type (Opportunity, Account, Contact...)
      operation="update",
      line_ending="LF",      # LF by default
      report_builder=FileReport(output=csvfile.name),
      external_key=None,     # External key ID, optional, None by default
      silent=False,          # IO Logger, optional, False by default,
  )
```
