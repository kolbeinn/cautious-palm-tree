from flask import Flask
from flask import request
from images import get_image_metadata

app = Flask(__name__)


@app.route("/img", methods=["POST"])
def img():
    """Endpoint that returns image metadata given a URL to an image"""
    imgurl = request.args.get("imgurl")
    if imgurl is None:
        return {
            "error": "you must supply an image URL through the 'imgurl' URL param",
        }
    return get_image_metadata(imgurl)
