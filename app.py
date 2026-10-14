import os
import uuid

import torch
from flask import Flask, render_template, request, send_from_directory
from PIL import Image
from transformers import BlipProcessor, BlipForConditionalGeneration
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder for uploaded images
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB upload limit
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "bmp", "webp"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Load the pretrained image-captioning model (once, at startup)
MODEL_NAME = "Salesforce/blip-image-captioning-base"
device = "cuda" if torch.cuda.is_available() else "cpu"
processor = BlipProcessor.from_pretrained(MODEL_NAME)
model = BlipForConditionalGeneration.from_pretrained(MODEL_NAME).to(device)
model.eval()


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    caption = None
    image_path = None
    error = None

    if request.method == "POST":
        # Check whether an image was uploaded
        if "image" not in request.files:
            error = "No image was uploaded."
            return render_template("index.html", caption=caption, image_path=image_path, error=error)

        file = request.files["image"]

        # Check whether a file was selected
        if file.filename == "":
            error = "Please select an image."
            return render_template("index.html", caption=caption, image_path=image_path, error=error)

        if not allowed_file(file.filename):
            error = "Unsupported file type. Please upload a PNG, JPG, GIF, BMP or WEBP image."
            return render_template("index.html", caption=caption, image_path=image_path, error=error)

        # Save uploaded image under a safe, unique name
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(save_path)

        # URL the browser can use to display the image (served by /uploads/<filename>)
        image_path = f"/uploads/{filename}"

        try:
            # Open and prepare the uploaded image
            image = Image.open(save_path).convert("RGB")

            # Process the image (no prompt needed)
            inputs = processor(images=image, return_tensors="pt").to(device)

            # Generate a caption automatically
            with torch.no_grad():
                outputs = model.generate(**inputs, max_new_tokens=50)

            caption = processor.decode(outputs[0], skip_special_tokens=True)

        except Exception as e:
            error = f"Error generating caption: {str(e)}"

    return render_template("index.html", caption=caption, image_path=image_path, error=error)


@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)


if __name__ == "__main__":
    app.run(debug=True)