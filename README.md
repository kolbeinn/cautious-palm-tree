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

## Exercise 1

The solution as is should satisfy exercise 1. I've also tagged the first commit that solves exercise 1 as "e1".

## Exercise 2

The solution should also satisfy exercise 2. It doesn't give a bounding box, though. I'm sure we could get it to do that
if we look closer at the ImageAI documentation/code. The first commit to satisfy the requirements in exercise 2 is tagged

## Exercise 3

I'm not going to have time to implement this feature. Given the time, I would probably have chosen something like DeepDream effects (see https://deepdreamgenerator.com/). I've always found generative computer vision more interesting than analytical
computer vision.

## Section B

There is a lot to be said about how to turn a toy service like the one I wrote into a full-fledged, production-ready service. I'm only going to be able to scratch the surface on any given topic. That being said, the first two areas I would spend time on before deploying to production are security and performance. The code is badly lacking in both, at least by production standards.

### Security

Major threats:
-denial of service attacks against this service
-using this service to DOS other websites
-injection attacks (we're taking in arbitrary strings from a potentially malicious user)

Here are a few issues we should address:
-input validation and sanitization
-rate limiting
-domain blocklisting

You might want to consider making this a service that requires signing up and creating a profile. Having it completely open is asking for trouble. 

### Performance

Top of mind issues:
-Stop writing images to disk on every request
-Use an object detection model designed for real-time use

### Infrastructure

The fastest way to deploy this to production would probably be to use Heroku or Amazon Elastic Beanstalk. That being said, if I expect to expand this service into a full-fledged app, I would probably want to completely change the infra. I'd use NodeJS+express/koa or Django instead of Flask. Flask is too barebones for my liking. Perfect for toy projects or large companies that want to do everything from scratch anyway. 

### Implementation

This is another big topic. I don't think I'm going to do it justice here. Look into Jenkins, github, gitlab as a starting point.

### Observability

You generally want at least three types of logging. Analytics logging (how is the service being used), error logging (what is breaking), and security logging (authentication events, who accesses what, failed authentications and access requests). Systems to consider include the ELK stack, Prometheus, and Grafana.

### Variable load

Constant demand is relatively easy and very rare in the wild. There is not much to deal with in that case. Spiky demand is typically either because there is a diurnal pattern to how the users interact with the service (e.g. everybody uses it right after work), or because there is a 'viral' aspect to it's use (suddenly everyone starts asking for metadata for the same image). The latter can be addressed with good caching. Caching will probably help less in the former case, so you'd just need to have infrastructure ready to handle the peak load.

### Data Persistence

The data in question is highly unstructured, so it stands to reason to use a nosql database like MongoDB or Elastisearch to persist the data. That being said, I believe PostgreSQL is actually really good at handling JSON and RDMS just offer so many convenient features that everybody misses when using nosql data stores. I'd probably use Postgres if at all practical and MongoDB otherwise.



