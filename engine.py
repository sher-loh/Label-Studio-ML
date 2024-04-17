import shutil
import uuid
from parser.compute import Compute
from pathlib import Path
from subprocess import run

from label_studio_ml.model import LabelStudioMLBase

from utils.gcs import download_public_file, get_metadata_from_url


class AssistedBoundingBox(LabelStudioMLBase):
    """Assisted Bounding Box Labelling Logic

    This class provides the model for labeling the videos with the generated bounding boxes for the frontend.

    :param from_name: A string representing source data block.
    :param to_name: A string representing target data block.
    :param labels : The list of labels to use for labeling the data.

    Sample format of the prediction is as follows:
    {
      "value": {
        "framesCount": number, total frames in video
        "duration": number, total duration of video
        "sequence": [
          {
            "frame": number,
            "rotation": number,
            "x": number,
            "y": number,
            "width": number,
            "height": number,
            "time": number
          },
          {
            "x": number,
            "y": number,
            "width": number,
            "height": number,
            "rotation": number,
            "frame": number,
            "time": number
          }
        ],
        "labels": string[]
      },
      "id": string,
      "from_name": string,
      "to_name": string,
      "type": string,
      "origin": string
    }
    """

    def __init__(self, **kwargs):
        """Initializes the AssistedBoundingBox model."""
        super(AssistedBoundingBox, self).__init__(**kwargs)
        # you can preinitialize variables with keys needed to extract info from tasks and annotations and form predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        self.from_name = from_name
        self.to_name = schema["to_name"][0]
        self.labels = schema["labels"]

    def predict(self, tasks, **kwargs):
        """Returns the list of predictions based on the input list of tasks.

        :param tasks: list of input tasks. An example is given as below:
          [{'id': 1908, 'data': {'video_url': 'gs://ucf-crime-dataset/Abuse/Abuse001_x264.mp4'}, 'meta': {}, 'created_at': '2023-04-29T14:47:06.171943Z', 'updated_at': '2023-04-29T14:47:06.171976Z', 'is_labeled': False, 'overlap': 1, 'inner_id': 1, 'total_annotations': 0, 'cancelled_annotations': 0, 'total_predictions': 0, 'comment_count': 0, 'unresolved_comment_count': 0, 'last_comment_updated_at': None, 'project': 3, 'updated_by': None, 'file_upload': None, 'comment_authors': [], 'annotations': [], 'predictions': []}]

        :return: A list of prediction as required by label studio
        """
        video_url = tasks[0]["data"]["video_url"]
        predictions = self._run_tracker(video_url)
        return [predictions]

    def _run_tracker(self, vid_path):
        """Runs the Yolov8 object tracking algorithm on the given video and returns the list of predictions.

        :param vid_path: path of the input video from GCS. An example is given as below:
          gs://ucf-crime-dataset/Abuse/Abuse001_x264.mp4

        :returns: A list of prediction as required by label studio
        """
        results = []
        # generate a random directory to store the video and model output
        DIR_PREFIX = str(uuid.uuid4())

        try:
            # make directory is does not exist
            Path(DIR_PREFIX).mkdir(parents=True, exist_ok=True)
            # get metadata from url passed in
            bucket_name, video_path, video_name = get_metadata_from_url(vid_path)
            video_destination = Path(f"{DIR_PREFIX}/{video_name}.mp4")
            model_output_destination = Path(f"{DIR_PREFIX}/{video_name}_results")

            # download video from GCS
            download_public_file(bucket_name, video_path, video_destination)

            # run yolov8 model
            command = f"python3 yolov8_tracking/track.py --source {video_destination} --save-txt --save-txt-path {model_output_destination}"
            run(command.split(), check=True)

            # run the compute script to parse the labels from Yolov8
            results = Compute(str(model_output_destination) + ".txt").process()
        except Exception as e:
            print("Error in running tracker with error: " + e)
        finally:
            # remove temp directory after successful / error run
            # this is used to ensure storage does not get filled up
            shutil.rmtree(DIR_PREFIX)
            return results
