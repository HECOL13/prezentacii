from flask import Flask, request, jsonify, send_file
from pptx import Presentation
from PIL import Image
import os
import uuid

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# 🔥 загрузка презентации
@app.route("/upload", methods=["POST"])
def upload():
    file = request.files["file"]
    file_id = str(uuid.uuid4())
    path = os.path.join(UPLOAD_FOLDER, file_id + ".pptx")
    file.save(path)

    prs = Presentation(path)

    slides = []

    for i, slide in enumerate(prs.slides):
        for shape in slide.shapes:
            if shape.shape_type == 13:  # IMAGE
                image = shape.image
                img_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_{i}.png")
                
                with open(img_path, "wb") as f:
                    f.write(image.blob)

                slides.append(img_path)

    return jsonify({
        "id": file_id,
        "slides": slides
    })


# 🔥 скачать готовую презентацию
@app.route("/download/<file_id>")
def download(file_id):
    path = os.path.join(OUTPUT_FOLDER, file_id + ".pptx")
    return send_file(path, as_attachment=True)
