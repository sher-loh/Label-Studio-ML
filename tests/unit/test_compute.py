import json
import os
from parser.compute import Compute

import pytest


@pytest.fixture
def file_path():
    current_file = os.path.abspath(__file__)
    relative_path = "../../static/small_input.txt"
    absolute_path = os.path.abspath(os.path.join(current_file, relative_path))
    return absolute_path


def test_read_file(file_path):
    c = Compute(file_path=file_path)
    lines = c._read_file()
    assert len(lines) == 8


# Test for _group_by_id method
def test_group_by_id(file_path):
    c = Compute(file_path=file_path)
    lines = c._read_file()
    cluster = c._group_by_id(lines)

    assert len(cluster) == 4
    assert len(cluster[(1, 12)]) == 2
    assert len(cluster[(1, 13)]) == 1
    assert len(cluster[(1, 15)]) == 1
    assert len(cluster[(1, 6)]) == 4


# Test for _group_by_continuous_frames method
def test_group_by_continuous_frames(file_path):
    c = Compute(file_path=file_path)
    lines = c._read_file()
    cluster = c._group_by_id(lines)
    grouped_cluster = c._group_by_continuous_frames(cluster)

    assert len(grouped_cluster) == 4
    assert len(grouped_cluster[(1, 12)]) == 2
    assert len(grouped_cluster[(1, 13)]) == 1
    assert len(grouped_cluster[(1, 15)]) == 1
    assert len(grouped_cluster[(1, 6)]) == 2


# Test for _generate_ls_json method
def test_process(file_path):
    c = Compute(file_path=file_path)
    res = c.process()
    expected_result = {
        "result": [
            {
                "value": {
                    "sequence": [
                        {
                            "frame": 1,
                            "x": 38.125,
                            "y": 44.1667,
                            "width": 7.8125,
                            "height": 37.5,
                            "enabled": False,
                        },
                        {
                            "frame": 4,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": False,
                        },
                    ],
                    "labels": ["Parking meter"],
                },
                "from_name": "box",
                "to_name": "video",
                "type": "videorectangle",
                "origin": "yolov8",
            },
            {
                "value": {
                    "sequence": [
                        {
                            "frame": 100,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": False,
                        }
                    ],
                    "labels": ["People"],
                },
                "from_name": "box",
                "to_name": "video",
                "type": "videorectangle",
                "origin": "yolov8",
            },
            {
                "value": {
                    "sequence": [
                        {
                            "frame": 123,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": False,
                        }
                    ],
                    "labels": ["Car"],
                },
                "from_name": "box",
                "to_name": "video",
                "type": "videorectangle",
                "origin": "yolov8",
            },
            {
                "value": {
                    "sequence": [
                        {
                            "frame": 150,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": True,
                        },
                        {
                            "frame": 151,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": False,
                        },
                        {
                            "frame": 158,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": True,
                        },
                        {
                            "frame": 159,
                            "x": 37.8125,
                            "y": 41.6667,
                            "width": 7.5,
                            "height": 41.25,
                            "enabled": False,
                        },
                    ],
                    "labels": ["Car"],
                },
                "from_name": "box",
                "to_name": "video",
                "type": "videorectangle",
                "origin": "yolov8",
            },
        ]
    }

    assert res == expected_result
