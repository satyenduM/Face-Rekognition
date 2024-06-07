from utils import upload_file_to_storage, extract_folder_id

from flask import request, render_template
from lambda_functions import call_lambda_function
from flask import current_app as app
from flask import Flask
import os

def create_app():
    app = Flask(__name__, static_folder='static')

    @app.route("/", methods=["GET", "POST"])
    def home_route():
        if request.method == "POST":
            drive_link = request.form.get("drive_link")
            folder_id = extract_folder_id(drive_link)
            reference_image = request.files.get("reference_image")
            reference_image_id = upload_file_to_storage(reference_image)
            
            from celery_worker import process_images
            task = process_images.delay(folder_id, reference_image_id)
            
            return render_template("result.html", task_id=task.id)
        return render_template("home.html")
    
    @app.route("/task-status/<task_id>")
    def task_status(task_id):
        from celery.result import AsyncResult
        result = AsyncResult(task_id)
        return {"status": result.status, "result": result.result}
    
    return app
