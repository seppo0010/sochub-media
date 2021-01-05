FROM ubuntu:20.04
WORKDIR /code
ENV FLASK_APP=index.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN apt update && DEBIAN_FRONTEND=noninteractive apt install -y ffmpeg python3 python3-pip && apt clean
RUN pip3 install flask youtube-dl
EXPOSE 80
COPY . .
ENV FLASK_APP=index.py
CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]
