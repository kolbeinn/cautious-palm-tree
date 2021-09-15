# cautious-palm-tree

This is a simple toy service that returns a bunch of image metadata
given a URL to an image. In order to run it, you must
-Install the requirements listed in requirements.txt
-Retrieve a model file from https://github.com/OlafenwaMoses/ImageAI/releases/download/essentials-v5/resnet50_coco_best_v2.1.0.h5/ and save it to this directory

You can start the flask server by typing
```
FLASK_APP=server flask run
```

The service will be available on the local machine on port 5000. In order to query the service, you must send a post request
to the URI "http://localhost:5000/img?<image url>" where you replace <image url> with an actual image URL. You need to URL-encode
the <image url>.