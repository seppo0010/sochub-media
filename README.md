# sochub-media

Download GIFs from segments of youtube videos. It allows up to 10 seconds

## Sample usage

```
$ FLASK_ENV=development FLASK_APP=index.py flask run &
$ curl localhost:5000/video-to-gif -v --data end=10 --data url=https://www.youtube.com/watch\?v\=dQw4w9WgXcQ > sample.gif
```
