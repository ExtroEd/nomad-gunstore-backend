import cloudinary
import cloudinary.uploader
import os

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_KEY"),
    api_secret=os.getenv("CLOUDINARY_SECRET"),
    secure=True
)

def upload_logo():
    result = cloudinary.uploader.upload(
        "static/img/logo.png",
        public_id="nomad_logo",
        overwrite=True,
        folder="nomad"
    )
    return result["secure_url"]
