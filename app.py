#
# This is the main application file for the PDF Merger web app.
# It handles routing, file uploads, and PDF merging.
#
# To run this script:
# 1. Install Flask and PyPDF2: `pip install Flask PyPDF2`
# 2. Make sure this file (`app.py`) is in the root directory.
# 3. Ensure the `templates` directory with `index.html` and `merger.html` exists.
# 4. Run the application from your terminal: `flask run`
# 5. Open your web browser and go to http://127.0.0.1:5000
#

import os
import sys
import uuid
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template, send_file
from PyPDF2 import PdfMerger
from datetime import datetime

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    """Renders the home page with a link to the PDF merger."""
    return render_template("index.html")

@app.route("/merger", methods=["GET"])
def merger_page():
    """Renders the PDF merger application page."""
    return render_template("merger.html")

@app.route("/compress", methods=["GET"])
def compress_page():
    """Renders the PDF compress application page."""
    return render_template("compress.html")

@app.route("/convert", methods=["GET"])
def convert_page():
    """Renders the PDF convert application page."""
    return render_template("convert.html")

@app.route("/edit", methods=["GET"])
def edit_page():
    """Renders the PDF edit application page."""
    return render_template("edit.html")

@app.route("/sign", methods=["GET"])
def sign_page():
    """Renders the PDF sign application page."""
    return render_template("sign.html")

@app.route("/merge", methods=["POST"])
def merge_pdfs():
    """Handles the PDF file upload, merging, and downloading."""
    uploaded_files = request.files.getlist("pdfs")
    
    if not uploaded_files or len(uploaded_files) < 2:
        return {"error": "Please upload at least two PDF files."}, 400

    merger = PdfMerger()
    temp_files = []

    try:
        for file_storage in uploaded_files:
            # Create a unique temporary filename
            temp_filename = f"{uuid.uuid4()}.pdf"
            file_storage.save(temp_filename)
            temp_files.append(temp_filename)
            merger.append(temp_filename)

        # Create a unique name for the final merged PDF
        output_filename = f"merged_{uuid.uuid4()}.pdf"
        with open(output_filename, "wb") as output_file:
            merger.write(output_file)

        # Send the merged file to the user for download
        return send_file(output_filename, as_attachment=True, mimetype='application/pdf')

    except Exception as e:
        # Catch any errors and return a JSON error message
        return {"error": str(e)}, 500
    finally:
        merger.close()
        # Clean up temporary files
        for filename in temp_files:
            if os.path.exists(filename):
                os.remove(filename)
        # Clean up the final merged file after it's sent
        if 'output_filename' in locals() and os.path.exists(output_filename):
            os.remove(output_filename)

@app.route("/compress", methods=["POST"])
def compress_pdfs():
    """Handles the PDF file upload, merging, and downloading."""
    uploaded_files = request.files.getlist("pdfs")
    
    if not uploaded_files or len(uploaded_files) < 2:
        return {"error": "Please upload at least two PDF files."}, 400
    
if __name__ == "__main__":
    app.run(debug=True, port=5001)
