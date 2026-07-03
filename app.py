from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename
from processing import reduce_noise
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "outputs"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["OUTPUT_FOLDER"] = OUTPUT_FOLDER

# Create folders if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/upload", methods=["POST"])
def upload():

    if "audio" not in request.files:
        return "No audio file selected."

    file = request.files["audio"]

    if file.filename == "":
        return "Please select a WAV file."

    # Safe filename
    filename = secure_filename(file.filename)

    input_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)

    output_filename = "clean_" + filename

    output_path = os.path.join(app.config["OUTPUT_FOLDER"], output_filename)

    # Save uploaded file
    file.save(input_path)

    # Process audio
    reduce_noise(input_path, output_path)

    # Show result page
    return render_template(
        "result.html",
        original=filename,
        cleaned=output_filename
    )


@app.route("/uploads/<path:filename>")
def uploaded_file(filename):
    return send_from_directory(
        app.config["UPLOAD_FOLDER"],
        filename
    )


@app.route("/outputs/<path:filename>")
def output_file(filename):
    return send_from_directory(
        app.config["OUTPUT_FOLDER"],
        filename
    )


@app.route("/download/<path:filename>")
def download(filename):
    return send_from_directory(
        app.config["OUTPUT_FOLDER"],
        filename,
        as_attachment=True
    )


if __name__ == "__main__":
    app.run(debug=True)