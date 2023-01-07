FROM opendronemap/odm:latest

WORKDIR /

COPY tasks.sh requirements.txt ./
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && pip3 install -r requirements.txt

COPY run.py Coarsening.py fill_holes.py /code/

ENTRYPOINT ["bash","tasks.sh"]
