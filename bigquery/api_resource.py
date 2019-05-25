__author__ = 'bobo'


# library installation
# https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python


# long running operations
#https://googlecloudplatform.github.io/google-cloud-python/stable/operation-api.html
# poll() function to keep checking the running of the operations


# api example python
# https://github.com/tylertreat/BigQuery-Python

from bigquery import get_client

# # Imports the Google Cloud client library
# from google.cloud import bigquery
#
# # Instantiates a client
# bigquery_client = bigquery.Client()
#
# # The name for the new dataset
# dataset_name = 'my_new_dataset'
#
# # Prepares the new dataset
# dataset = bigquery_client.dataset(dataset_name)
#
# # Creates the new dataset
# dataset.create()
#
# print('Dataset {} created.'.format(dataset.name))
