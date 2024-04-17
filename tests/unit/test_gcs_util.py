from utils.gcs import get_metadata_from_url

BUCKET = "ucf-crime-dataset"
TEST_VIDEO = "Assault/Assault038_x264.mp4"

def test_get_metadata_from_url():
    url = f"gs://{BUCKET}/{TEST_VIDEO}"
    assert get_metadata_from_url(url) == (BUCKET, TEST_VIDEO, "Assault038_x264.mp4")