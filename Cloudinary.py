import os, cloudinary, requests
from cloudinary import api, Search

def list_images():
    cloudinary.config(
        cloud_name="dlmntdz7q",
        api_key=os.environ.get("CLOUDINARY_API_KEY"),
        api_secret=os.environ.get("CLOUDINARY_API_SECRET")
    )

    result = Search().expression('folder:Marley_Gallery/*').execute()
    url_list = []
    for image in result['resources']:
        url_list.append(image['secure_url'])
    return url_list
