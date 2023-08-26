FROM python:3.11-slim-bookworm

# set working directory
RUN mkdir -p /usr/src/twoface/models/mediapipe
COPY . /usr/src/twoface/
WORKDIR /usr/src/twoface

RUN pip install --upgrade pip 
# apt update, apt search wget, apt info wget, apt install wget
RUN apt update && apt install wget libgl1 libglib2.0-0 libsm6 libxext6  -y
RUN python -m pip install -e ".[dev]"
RUN wget -O models/face_landmarker_v2_with_blendshapes.task -q https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task
