from google.cloud import storage


def download_public_file(bucket_name, source_blob_name, destination_file_name):
    """Downloads a public blob from the bucket."""

    storage_client = storage.Client.create_anonymous_client()

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)


def get_metadata_from_url(url):
    paths = url.split("/")
    bucket_name = paths[2]
    video_path = "/".join(paths[3:])
    video_name = paths[-1]

    return bucket_name, video_path, video_name
