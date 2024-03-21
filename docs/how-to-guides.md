# Installation
To install `py-motion-detection` run: 

```shell
poetry install
``` 

# Running the tests
To run all the tests:

```shell
poetry run pytest tests
```

# Generating the documentation
To read the project's documentation run:

```shell
poetry run mkdocs serve
```

and click on this [link](http://127.0.0.1:8000/).

# Usage

## Command line interfaces

### Running the motion detection and data logging app

The `py-motion-detection` CLI will start the motion detection app.
To see all the available options of the `py-motion-detection` app run:

```shell
py_motion_detector --help
```

Example usage: 
```shell
py_motion_detector -p $HOME/Downloads/motion_detected_frames/ -r 800 -m 500 -t 4 -l /tmp/log -i INFO
```

### Logged data player

The `py_motion_detector_data_player` CLI can be used to replay the stored frames and their bounding boxes. 

To see all the available options run: 

```shell
py_motion_detector_data_player --help
```

Example usage: 
```shell
py_motion_detector_data_player -p $HOME/Downloads/motion_detected_frames/ -w 500 -l
```


# Running on a raspberry pi

## Linux Prerequisites

```shell 
sudo apt-get install libatlas-base-dev
```

```shell
sudo apt-get install libjasper-dev
```

```shell
sudo apt-get install libqtgui4
```

```shell
sudo apt-get install python3-pyqt5
```

```shell
sudo apt install libqt4-test
```

## To access the camera with OpenCV

Run the following before running the python script:
```shell 
sudo modprobe bcm2835-v4l2
```
