# third party API but not official API

#https://github.com/tylertreat/BigQuery-Python
from bigquery import get_client

from oauth2client.service_account import ServiceAccountCredentials

# BigQuery project id as listed in the Google Developers Console.
project_id = 'robert-kraut-1234'

# Service account email address as listed in the Google Developers Console.
service_account = 'bowen-yu@robert-kraut-1234.iam.gserviceaccount.com'

# PKCS12 or PEM key provided by Google.
key_file = '/Users/bobo/Documents/wikipedia_user_dropout/data/RobertKraut-CMU-afc8b526c044.json'

# client = get_client(project_id, service_account=service_account, private_key_file=key_file, readonly=True)

# JSON key provided by Google
# json_key = 'key.json'
json_key = "/Users/bobo/Documents/wikipedia_user_dropout/data/RobertKraut-CMU-afc8b526c044.json"

client = get_client(project_id, service_account=service_account, json_key_file=json_key, readonly=False)


# Create a new table.
schema = [
    {'name': 'foo', 'type': 'STRING', 'mode': 'nullable'},
    {'name': 'bar', 'type': 'FLOAT', 'mode': 'nullable'}
]

## TODO: open issue of the project - No handlers could be found for logger "bigquery.client"
# details: https://github.com/tylertreat/BigQuery-Python/issues/103
created = client.create_table('bowen_editor_attachments', 'my_table', schema)
print(created)

exists = client.check_table('bowen_editor_attachments', 'my_table')
print (exists)

## TODO: Need admin to run query jobs - details: https://cloud.google.com/bigquery/docs/access-control
# Submit an async query.
job_id, _results = client.query('SELECT * FROM bowen_editor_attachments.users_valid LIMIT 1000')

# Check if the query has finished running.
complete, row_count = client.check_job(job_id)

# Retrieve the results.
results = client.get_query_rows(job_id)

print(results)


## sudo pip install pyopenssl --upgrade