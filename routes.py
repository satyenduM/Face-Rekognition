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
            # Upload the reference image to the initial S3 bucket
            reference_image_id = upload_file_to_storage(reference_image)  # Upload the reference image to storage
            # Call the driveToS3 lambda function with folder_id and bucket_name
            s3_bucket = call_lambda_function('driveToS3', {'folder_id': folder_id, 'bucket_name': 'face-rekognition2'})
            # Specify the bucket name where the reference image should be uploaded
            initial_s3_bucket = 'face-rekognition2'
            # Call the face_rekog_adv lambda function
            result_bucket = call_lambda_function('face_rekog_adv', {'source_bucket': initial_s3_bucket, 'source_image': reference_image_id, 'target_bucket': 'resultbucket0'})  # Call the face recognition lambda function
            # Call the zipS3Bucket lambda function
            download_url = call_lambda_function('zipS3Bucket', {'s3_bucket_name': 'resultbucket0'})  # Zip the result bucket and get the download URL
            
            return render_template("result.html", download_url=download_url)
        return render_template("home.html")
    
    return app