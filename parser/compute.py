import random


class FrameData:
    """
    Represents data for a single frame of a video.
    """

    def __init__(self, frame_id, id, x, y, w, h, label, label_id):
        """
        Initializes a new FrameData object.

        :param frame_id: the ID of the frame
        :param id: the ID of the object in the frame
        :param x: the x-coordinate of the object's bounding box
        :param y: the y-coordinate of the object's bounding box
        :param w: the width of the object's bounding box
        :param h: the height of the object's bounding box
        :param label: the label of the object
        :param label_id: the ID of the label
        """
        self.frame_id = int(frame_id)
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

        # Capitalize the first letter of the label
        self.label = label.capitalize()
        self.label_id = int(label_id)

    def generate_frame_json(self, interpolation=False):
        """
        Generates a JSON object representing the FrameData object.

        :param interpolation: whether or not the object is being interpolated (True represent start of continuous frames, False represents end of continuous frames)
        :return: the generated JSON object compatible with Label Studio
        """
        return {
            "frame": self.frame_id,
            "x": self.x,
            "y": self.y,
            "width": self.w,
            "height": self.h,
            "enabled": interpolation,
        }

    def __str__(self):
        """
        Returns a string representation of the FrameData object in JSON format.

        :return: the string representation
        """
        return f"frame_id: {self.frame_id}, id: {self.id}, x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}, label: {self.label}, label_id: {self.label_id}"


class Compute:
    """
    Performs computation on the data in the input file to generate a JSON output.
    """

    def __init__(self, file_path=None):
        """
        Initializes a new Compute object.

        :param file_path: the path to the input file
        """
        self.file_path = file_path

    def _read_file(self):
        """
        Reads the input file and returns its contents as a list of lines.

        :return: the list of lines
        """
        with open(self.file_path) as f:
            lines = f.readlines()
        return lines

    def _group_by_id(self, lines):
        """
        Groups the FrameData objects in the input lines by object ID and label ID.

        :param lines: the list of input lines
        :return: the dictionary of grouped FrameData objects
        """
        cluster = {}
        for line in lines:
            # strip to remove trailing newline
            line = line.strip()
            frame_id, id, x, y, w, h, _, _, _, _, label, label_id = line.split(",")
            frame = FrameData(frame_id, id, x, y, w, h, label, label_id)

            # grouping by two keys - frame_id and label_id (treated as primary key)
            if (frame.id, frame.label_id) not in cluster:
                cluster[(frame.id, frame.label_id)] = []
            cluster[(frame.id, frame.label_id)].append(frame)
        return cluster

    def _group_by_continuous_frames(self, cluster):
        """
        Groups the FrameData objects in the input cluster by continuous frames. Object that is present in consecutive frames
        are grouped together.

        :param cluster: the dictionary of grouped FrameData objects
        :return: the dictionary of grouped FrameData objects by continuous frames
        """
        grouped_cluster = {}
        for (id, label_id), frames in cluster.items():
            groups, group = [], []
            for i, frame in enumerate(frames):
                if i == 0:
                    # no previous group to compare with here
                    # so we just add the first frame to the group
                    group.append(frame)
                else:
                    prev_frame = group[-1]
                    # if the current frame is consecutive to the previous frame
                    # we add it to the group
                    # otherwise, we start a new group
                    if prev_frame.frame_id + 1 == frame.frame_id:
                        group.append(frame)
                    else:
                        groups.append(group)
                        group = [frame]

            groups.append(group)
            grouped_cluster[(id, label_id)] = groups
        return grouped_cluster

    def _generate_ls_json(self, grouped_cluster):
        """
        Generates a JSON object representing the input grouped cluster.

        :param grouped_cluster: the dictionary of grouped FrameData objects by continuous frames
        :return: JSON prediction object in label-studio format
        """
        results = []
        for (id, label_id), groups in grouped_cluster.items():
            sequence = []
            obj_name = None
            # iterate over groups of continuous frames
            for group in groups:
                for i in range(len(group)):
                    frame = group[i]
                    # set the object name to the label of the first frame in the group
                    if obj_name is None:
                        obj_name = frame.label

                    if len(group) == 1:
                        sequence.append(frame.generate_frame_json(interpolation=False))
                        continue
                    is_last = i == len(group) - 1
                    # if the group has more than one frame, we interpolate the frames
                    # by setting the enabled property to False for all frames except the first and last
                    sequence.append(frame.generate_frame_json(interpolation=(not is_last)))
            
            # append sequence in label studio compatible format
            results.append(
                {
                    "value": {"sequence": sequence, "labels": [obj_name]},
                    "from_name": "box",
                    "to_name": "video",
                    "type": "videorectangle",
                    "origin": "yolov8",
                }
            )
        return {"result": results}

    def process(self):
        """
        Reads the input file, groups the FrameData objects, groups the FrameData objects by continuous frames,
        and generates a JSON object representing the grouped cluster.

        :return:  JSON prediction object in label-studio format
        """
        lines = self._read_file()
        cluster = self._group_by_id(lines)
        grouped_cluster = self._group_by_continuous_frames(cluster)
        json_result = self._generate_ls_json(grouped_cluster)
        return json_result

    def pretty_print_grouped_cluster(self, grouped_cluster):
        """
        Pretty prints the input grouped cluster for debugging purposes.

        :param grouped_cluster: the dictionary of grouped FrameData objects by continuous frames
        """
        for (id, label_id), groups in grouped_cluster.items():
            print(f"ID: {id}, Label ID: {label_id}")
            for group in groups:
                print("--------------------------------")
                for frame in group:
                    print(frame, sep=" ")
            print("\n")


if __name__ == "__main__":
    compute = Compute(file_path="examples/test_medium_input.txt")
    json_result = compute.process()
    print(json_result)
