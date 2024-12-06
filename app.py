from flask import Flask, request, jsonify
from utils import (
    concatenate_non_empty_cells_from_file,
    save_to_file,
    concatenate_non_empty_cells_stream,
)
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)


@app.route("/concatenate", methods=["POST"])
def concatenate_non_empty_cells_api():
    if "file" not in request.files:
        return "No file part", 400

    file = request.files["file"]

    if file.filename == "":
        return "No selected file", 400

    try:
        result_df = concatenate_non_empty_cells_stream(file.stream)
    except ValueError as e:
        logger.error("Error processing request: %s", e)
        return str(e), 400

    output_json = result_df.to_json(orient="records")
    return jsonify(output_json)


if __name__ == "__main__":
    mode = os.getenv("MODE", "api")
    if mode == "local":
        # Ask the user to provide the input file path
        input_file_path = input("Please provide the input file path: ")

        # Use the same path for the output file
        output_file_path = input_file_path

        df = concatenate_non_empty_cells_from_file(input_file_path)
        save_to_file(df, output_file_path)
    else:
        app.run(host="0.0.0.0", port=5000)
