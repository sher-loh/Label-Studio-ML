from parser.compute import FrameData

import pytest


def test_frame_data_init():
    frame = FrameData(1, 2, 3, 4, 5, 6, "label", 7)
    assert frame.frame_id == 1
    assert frame.id == 2
    assert frame.x == 3.0
    assert frame.y == 4.0
    assert frame.w == 5.0
    assert frame.h == 6.0
    assert frame.label == "Label"
    assert frame.label_id == 7


def test_frame_data_generate_frame_json():
    frame = FrameData(1, 2, 3, 4, 5, 6, "label", 7)
    json = frame.generate_frame_json(interpolation=True)
    assert json == {
        "frame": 1,
        "x": 3.0,
        "y": 4.0,
        "width": 5.0,
        "height": 6.0,
        "enabled": True,
    }


def test_frame_data_str():
    frame = FrameData(1, 2, 3, 4, 5, 6, "label", 7)
    string = str(frame)
    assert (
        string
        == "frame_id: 1, id: 2, x: 3.0, y: 4.0, w: 5.0, h: 6.0, label: Label, label_id: 7"
    )
