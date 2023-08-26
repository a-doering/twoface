# TwoFace
Combine the faces from two different photos that you upload.

## Run with docker
```sh
# Build docker image
docker build -f Dockerfile -t twoface .
# Run docker development container
docker run --name twoface_dev -v ${PWD}:/usr/src/twoface/ -p 7860:7860 -ti twoface /bin/bash 
# Run docker production container
docker run --name twoface_prod -v ${PWD}:/usr/src/twoface/ -p 7860:7860 -ti twoface /bin/bash

# Run gradio app in docker container
gradio app.py
```