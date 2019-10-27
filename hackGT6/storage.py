from google.cloud import storage

client = storage.Client()
bucket = client.get_bucket('<your-bucket-name>')
blob = bucket.blob('temp.jpg')
blob.upload_from_string('this is test content!')
