import requests
import pytest
import os

ML_BACKEND = os.environ.get("ML_BACKEND", "")


@pytest.fixture
def setup_schema():
    SCHEMA = """<View>
  <Video name="video" value="$video_url" sync="audio" framerate="30"/>
  <Labels name="caption" toName="audio">
    <Label value="Selection 1" background="#1BB500"/>
    <Label value="Selection 2" background="#FFA91D"/>
    <Label value="Selection 3" background="#358EF3"/>
    <Label value="Selection 4" background="#FF0000"/>
    <Label value="Selection 5" background="#800080"/>
  </Labels>
  <AudioPlus name="audio" value="$video_url" sync="video" speed="false"/>
  <View visibleWhen="region-selected">
    <Header value="Transcription"/>
    <TextArea name="transcription" toName="audio" editable="true" perRegion="true" required="true" maxSubmissions="1" rows="5" placeholder="Please provide a detailed caption specific to the scene"/>
  </View>
  <View>
    <VideoRectangle name="box" toName="video" smart="true"/>
    <Labels name="videoLabels" toName="video">
      <Label value="Person"/>
      <Label value="Bicycle"/>
      <Label value="Car"/>
      <Label value="Motorcycle"/>
      <Label value="Airplane"/>
      <Label value="Bus"/>
      <Label value="Train"/>
      <Label value="Truck"/>
      <Label value="Boat"/>
      <Label value="Traffic light"/>
      <Label value="Fire hydrant"/>
      <Label value="Stop sign"/>
      <Label value="Parking meter"/>
      <Label value="Bench"/>
      <Label value="Bird"/>
      <Label value="Cat"/>
      <Label value="Dog"/>
      <Label value="Horse"/>
      <Label value="Sheep"/>
      <Label value="Cow"/>
      <Label value="Elephant"/>
      <Label value="Bear"/>
      <Label value="Zebra"/>
      <Label value="Giraffe"/>
      <Label value="Backpack"/>
      <Label value="Umbrella"/>
      <Label value="Handbag"/>
      <Label value="Tie"/>
      <Label value="Suitcase"/>
      <Label value="Frisbee"/>
      <Label value="Skis"/>
      <Label value="Snowboard"/>
      <Label value="Sports ball"/>
      <Label value="Kite"/>
      <Label value="Baseball bat"/>
      <Label value="Baseball glove"/>
      <Label value="Skateboard"/>
      <Label value="Surfboard"/>
      <Label value="Tennis racket"/>
      <Label value="Bottle"/>
      <Label value="Wine glass"/>
      <Label value="Cup"/>
      <Label value="Fork"/>
      <Label value="Knife"/>
      <Label value="Spoon"/>
      <Label value="Bowl"/>
      <Label value="Banana"/>
      <Label value="Apple"/>
      <Label value="Sandwich"/>
      <Label value="Orange"/>
      <Label value="Broccoli"/>
      <Label value="Carrot"/>
      <Label value="Hot dog"/>
      <Label value="Pizza"/>
      <Label value="Donut"/>
      <Label value="Cake"/>
      <Label value="Chair"/>
      <Label value="Couch"/>
      <Label value="Potted plant"/>
      <Label value="Bed"/>
      <Label value="Dining table"/>
      <Label value="Toilet"/>
      <Label value="Laptop"/>
      <Label value="Mouse"/>
      <Label value="Remote"/>
      <Label value="Keyboard"/>
      <Label value="Cell phone"/>
      <Label value="Microwave"/>
      <Label value="Oven"/>
      <Label value="Toaster"/>
      <Label value="Sink"/>
      <Label value="Refrigerator"/>
      <Label value="Book"/>
      <Label value="Clock"/>
      <Label value="Vase"/>
      <Label value="Scissors"/>
      <Label value="Teddy bear"/>
      <Label value="Hair drier"/>
      <Label value="Toothbrush"/>
      <Label value="Tv" />
    </Labels>
  </View>
</View>"""

    data = {
        "project": "testing",
        'schema': SCHEMA,
        'hostname': "http://localhost:8080",
        'access_token': '1234567890123456789012345678901234567890'
    }
    return data

@pytest.mark.first
def test_basic_health_check():
    response = requests.get("http://127.0.0.1:9090/")
    assert response.status_code == 200

    response = requests.get("http://127.0.0.1:9090/health")
    assert response.status_code == 200

@pytest.mark.second 
def test_setup_object_detection(setup_schema):
    print(setup_schema)
    response = requests.post("http://127.0.0.1:9090/setup", json=setup_schema)
    assert response.status_code == 200

def test_versions():
    response = requests.post("http://127.0.0.1:9090/versions", json={"project": "testing"})
    assert response.status_code == 200

"""
Do not run this task unless you have a GPU, if not it will take a long time to even process this 10s video. 
"""
def test_prediction_success():
    tasks = [{'id': 1908, 'data': {'video_url': 'gs://ucf-crime-dataset/Abuse/Abuse029_x264.mp4'}, 'meta': {}, 'created_at': '2023-04-29T14:47:06.171943Z', 'updated_at': '2023-04-29T14:47:06.171976Z', 'is_labeled': False, 'overlap': 1, 'inner_id': 1, 'total_annotations': 0, 'cancelled_annotations': 0, 'total_predictions': 0, 'comment_count': 0, 'unresolved_comment_count': 0, 'last_comment_updated_at': None, 'project': 3, 'updated_by': None, 'file_upload': None, 'comment_authors': [], 'annotations': [], 'predictions': []}]
    response = requests.post("http://127.0.0.1:9090/predict", json= {
      'tasks': tasks,
    })

    assert response.status_code == 200

def test_prediction_fail():
    tasks = [{'id': 1908, 'data': {'video_url': 'non-existent'}, 'meta': {}, 'created_at': '2023-04-29T14:47:06.171943Z', 'updated_at': '2023-04-29T14:47:06.171976Z', 'is_labeled': False, 'overlap': 1, 'inner_id': 1, 'total_annotations': 0, 'cancelled_annotations': 0, 'total_predictions': 0, 'comment_count': 0, 'unresolved_comment_count': 0, 'last_comment_updated_at': None, 'project': 3, 'updated_by': None, 'file_upload': None, 'comment_authors': [], 'annotations': [], 'predictions': []}]
    response = requests.post("http://127.0.0.1:9090/predict", json= {
      'tasks': tasks,
    })

    # If the video does not exist, it should return an empty array
    assert response.json()['results'] == [[]]