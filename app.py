from flask import Flask, request, jsonify
from marker.converters.pdf import PdfConverter
from marker.models import create_model_dict
from marker.output import text_from_rendered
import os
import logging
import base64
from io import BytesIO

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB limit

# Ensure upload folder exists
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@app.route("/convert", methods=["POST"])
def convert_pdf():
    if "file" not in request.files:
        logger.error("No file provided in request")
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    if file.filename == "":
        logger.error("Empty filename provided")
        return jsonify({"error": "Empty filename"}), 400

    # Create a unique directory for this conversion
    conversion_id = os.urandom(8).hex()
    conversion_dir = os.path.join(app.config["UPLOAD_FOLDER"], conversion_id)
    os.makedirs(conversion_dir, exist_ok=True)

    # Save file with absolute path
    filepath = os.path.abspath(os.path.join(conversion_dir, file.filename))
    file.save(filepath)

    try:
        logger.info(f"Processing file: {file.filename}")
        converter = PdfConverter(artifact_dict=create_model_dict())
        rendered = converter(filepath)
        text, _, image_paths = text_from_rendered(rendered)

        # Log the image paths
        logger.info(f"Image paths: {image_paths}")

        # Convert PIL Image objects to base64
        encoded_images = []
        for img_name, img in image_paths.items():
            try:
                buffered = BytesIO()
                img.save(buffered, format="PNG")  # Save PIL Image to BytesIO
                encoded_image = base64.b64encode(buffered.getvalue()).decode("utf-8")
                encoded_images.append(encoded_image)
                logger.info(f"Successfully encoded image: {img_name}")
            except Exception as e:
                logger.error(f"Error encoding image {img_name}: {str(e)}")

        response = {
            "status": "success",
            "data": {
                "text": text,
                "images": encoded_images,
                "filename": file.filename,
                "filesize": os.path.getsize(filepath),
            },
        }
        logger.info(f"Successfully processed file: {file.filename}")
        return jsonify(response)
    finally:
        # Clean up
        if os.path.exists(conversion_dir):
            for temp_file in os.listdir(conversion_dir):
                try:
                    os.remove(os.path.join(conversion_dir, temp_file))
                except Exception as e:
                    logger.error(f"Error removing temp file: {str(e)}")
            os.rmdir(conversion_dir)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
