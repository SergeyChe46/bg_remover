import cv2
import os
from rembg import remove
from PIL import Image
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

UPLOAD_FOLDER = "static/uploads"
ALLOWED_EXTENSIONS = set(["png", "jpg", "jpeg", "webp"])

# Создание папок
if "static" not in os.listdir("."):
    os.mkdir("static")

if "uploads" not in os.listdir("static/"):
    os.mkdir("static/uploads")

# Настройки приложения
app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.secret_key = "39CM,9I,49dsa321@ERX"


# Файл имеет расширение и оно допустимо
def allowed_file(filename: str):
    return "." in filename and filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


# Убирает задний фон
def remove_background(input_path, output_path):
    input = Image.open(input_path)
    output = remove(input)
    output.save(output_path)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/remback", methods=["POST"])
def remback():
    file = request.files["file"]
    if file and allowed_file(file.filename):
        # Парсит путь до файла и составляет новое имя файла
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        # Новое имя файла для файла без заднего фона
        rembg_filename = filename.split(".")[0] + "_rembg.png"
        remove_background(
            UPLOAD_FOLDER + "/" + filename, UPLOAD_FOLDER + "/" + rembg_filename
        )
        return render_template(
            "home.html", org_img_name=filename, rembg_img_name=rembg_filename
        )


if __name__ == "main":
    app.run(debug=True)
