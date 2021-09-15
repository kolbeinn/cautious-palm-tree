import requests
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO
from imageai.Detection import ObjectDetection
import os
import numpy as np

# Initialize object detector
detector = ObjectDetection()
detector.setModelTypeAsRetinaNet()
detector.setModelPath(os.path.join(
    os.getcwd(), "resnet50_coco_best_v2.1.0.h5"))
detector.loadModel()


def get_image_metadata(url):
    response = requests.get(url)

    result = {
        "url": url,
        "status_code": response.status_code,
    }

    # Extract basic metadata
    try:
        image = Image.open(BytesIO(response.content))
        result.update(extract_basic_metadata(image))
        result["objects"] = detect_objects(image)
    except:
        # The world's most helpful error message
        result["error"] = "Something went wrong"

    return result


def extract_basic_metadata(image):
    """Extract basic metadata exposed by PIL"""
    exif_data = extract_exif_metadata(image)
    # Filter out binary data so we can JSON-serialize the results.
    pil_info = {k: v for k, v in image.info.items()
                if not isinstance(v, bytes)}
    return {
        "format": image.format,
        "format_description": image.format_description,
        "size": image.size,
        "mode": image.mode,
        "height": image.height,
        "width": image.width,
        "PIL_info": pil_info,
        "exif_data": exif_data,
    }


def extract_exif_metadata(image):
    """ Thanks to 
    https://www.thepythoncode.com/article/extracting-image-metadata-in-python
    for the code snippet"""
    exifdata = image.getexif()
    result = {}
    for tag_id in exifdata:
        # Convert to human readable data
        tag = TAGS.get(tag_id, tag_id)
        data = exifdata.get(tag_id)
        if isinstance(data, bytes):
            data = data.decode()
        result[tag] = data
    return result


def detect_objects(image):
    # Saving the image to disk here, because that's the fastest way to get this code to work.
    # IRL, I'd make this work without disk writes
    image.save("temp.jpg")
    """ Based on the sample code in 
    https://towardsdatascience.com/object-detection-with-10-lines-of-code-d6cb4d86f606"""
    execution_path = os.getcwd()
    detections = detector.detectObjectsFromImage(input_image=os.path.join(
        execution_path, "temp.jpg"), output_image_path=os.path.join(execution_path, "imagenew.jpg"))
    result = [{'name': ob["name"], 'probability': ob["percentage_probability"]}
              for ob in detections]
    return result
