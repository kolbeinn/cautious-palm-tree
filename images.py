import requests
import PIL
from PIL import Image
from PIL.ExifTags import TAGS
from io import BytesIO


def get_image_metadata(url):
    # First attempt to fetch the image
    response = requests.get(url)

    result = {
        "url": url,
        "status_code": response.status_code,
    }

    # Extract basic metadata
    try:
        image = Image.open(BytesIO(response.content))
        result.update(extract_basic_metadata(image))
    except PIL.UnidentifiedImageError as exc:
        # I know, I know, overly broad exception handling here
        result["error"] = exc.strerror

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
